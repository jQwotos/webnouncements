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
        if not self.userInfo: self.getUserInfo()

        school = self.request.get("s")
        if self.userInfo['user'] and self.userInfo['userInfo']:
            today = datetime.datetime.now()
            schoolInfo, linkInfo = SchoolAccount.getLinkSC(self.userInfo['userInfo'].user_id, school)
            requests = Post.query(Post.school_uuid == schoolInfo.uuid, Post.approved == False, Post.denied == False).order(-Post.startDate).fetch(50)
            posts = Post.query(Post.school_uuid == schoolInfo.uuid, Post.approved == True, Post.endDate >= today).order(-Post.endDate).fetch(50)

            schoolAccount = linkInfo[0] if len(linkInfo) > 0 else None

            if schoolInfo:
                self.render('school.html', requests=requests, posts=posts, school_uuid = schoolInfo.uuid, school_code = school, schoolAccount = schoolAccount)
            else:
                logging.warning("User '%s' tried to access '%s' without having permissions." % (self.userInfo['userInfo'].user_id, schoolInfo.uuid))
                self.render("cloud.html", error="You don't belong to that school.")

        else:
            logging.warning("User tried to access cloud without being signed in.")
            self.render("cloud.html", error="Please login before accessing cloud.")

class Send(Handler):
    def post(self):
        if not self.userInfo: self.getUserInfo()

        data = json.loads(self.request.body)
        postQueryInfo = Post.query(Post.uuid == data['uuid']).fetch()
        post = postQueryInfo[0] if len(postQueryInfo) > 0 else None

        if SchoolAccount.verifyLink(self.userInfo['userInfo'].user_id, post.school_uuid):
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
        data = json.loads(self.request.body)
        if not self.userInfo: self.getUserInfo()

        if SchoolAccount.verifyLink(self.userInfo['userInfo'].user_id, data['school_uuid']):
            code = str(uuid4())
            invite = Invite(
                uuid = code,
                school_uuid = data['school_uuid'],
                createdBy = self.userInfo['userInfo'].user_id,
                uses = int(data['numInvites']),
            )
            invite.put()
            self.respondToJson({'code': code})

class Join(Handler):
    def post(self):
        if not self.userInfo: self.getUserInfo()
        inviteCode = self.request.get('ic')

        inviteQueryInfo = Invite.query(Invite.uuid == inviteCode).fetch()
        inviteInfo = inviteQueryInfo[0] if len(inviteQueryInfo) > 0 else None

        if inviteInfo and inviteInfo.uses > 0:
            if not SchoolAccount.verifyLink(self.userInfo['userInfo'].user_id, inviteInfo.school_uuid):
                schoolAccount = SchoolAccount(
                    user_id = self.userInfo['userInfo'].user_id,
                    school_uuid = inviteInfo.school_uuid,
                )
                inviteInfo.uses -= 0
                inviteInfo.put()
                schoolAccount.put()
                self.redirect('/cloud/main')

app = webapp2.WSGIApplication([
    (static_location + '/main', School),
    (static_location  + '/send', Send),
    (static_location + '/generateInvite', GenerateInvite),
    (static_location + '/join', Join),
], debug=True)
