import json
import datetime
import logging
from uuid import uuid4

import webapp2

from google.appengine.ext import ndb
from google.appengine.api import users

from ..supports.main import Handler
from ..supports.tables import Post, SchoolAccount, Invite, School, Account

static_location = '/school'

class School(Handler):
    def get(self):
        user = users.get_current_user()
        school = self.request.get("s")
        schoolInfo, linkInfo = SchoolAccount.getLinkSC(user.user_id(), school)

        schoolAccount = linkInfo[0] if len(linkInfo) > 0 else None

        if schoolInfo:
            self.render('school.html', school_uuid = schoolInfo.uuid, school_code = school, schoolAccount = schoolAccount)
        else:
            logging.warning("User '%s' tried to access '%s' without having permissions." % (user.user_id(), schoolInfo.uuid))
            self.render("cloud.html", error="You don't belong to that school.")

class Send(Handler):
    def post(self):
        user = users.get_current_user()

        data = json.loads(self.request.body)
        postQueryInfo = Post.query(Post.uuid == data['uuid']).fetch()
        post = postQueryInfo[0] if len(postQueryInfo) > 0 else None

        if SchoolAccount.verifyLink(user.user_id(), post.school_uuid):
            if data['action'] == 'deny':
                post.approved = False
                post.denied = True
                post.put()
            elif data['action'] == 'approve':
                post.approved = True
                post.denied = False
                post.put()

class GenerateInvite(Handler):
    def post(self):
        user = users.get_current_user()
        data = json.loads(self.request.body)

        if SchoolAccount.verifyLink(user.user_id(), data['school_uuid']):
            code = str(uuid4())
            invite = Invite(
                uuid = code,
                school_uuid = data['school_uuid'],
                createdBy = user.user_id(),
                uses = int(data['numInvites']),
            )
            invite.put()
            self.respondToJson({'code': code})

class Join(Handler):
    def add(self, inviteCode):
        user = users.get_current_user()
        inviteQueryInfo = Invite.query(Invite.uuid == inviteCode).fetch()
        inviteInfo = inviteQueryInfo[0] if len(inviteQueryInfo) > 0 else None

        if inviteInfo and inviteInfo.uses > 0:
            if not SchoolAccount.verifyLink(user.user_id(), inviteInfo.school_uuid):
                schoolAccount = SchoolAccount(
                    user_id = user.user_id(),
                    school_uuid = inviteInfo.school_uuid,
                )
                inviteInfo.uses -= 0
                inviteInfo.put()
                schoolAccount.put()
                self.redirect('/cloud/main')

    def get(self):
        inviteCode = self.request.get('ic')
        user = users.get_current_user()

        if user:
            self.add(inviteCode)
        else:
            self.redirect(users.create_login_url('%s/join?ic=%s' % (static_location, inviteCode)))
    def post(self):
        user = users.get_current_user()
        inviteCode = self.request.get('ic')
        self.add(inviteCode)

app = webapp2.WSGIApplication([
    (static_location + '/main', School),
    (static_location  + '/send', Send),
    (static_location + '/generateInvite', GenerateInvite),
    (static_location + '/join', Join),
], debug=True)
