import json
import datetime
from uuid import uuid4

import webapp2

from google.appengine.ext import ndb
from google.appengine.api import users

from ..supports.main import Handler
from ..supports.tables import Post, SchoolAccount, Invite, School, Account
from ..supports.tabler import verifyLink

static_location = '/school'

class School(Handler):
    def get(self):
        user = self.getUserInfo()
        school = self.request.get("s")
        if user['user'] and user['userInfo']:
            today = datetime.datetime.now()
            schoolInfo = SchoolAccount.getLinkSC(user['userInfo'].user_id, school)
            requests = Post.query(Post.school_uuid == schoolInfo.uuid, Post.approved == False, Post.denied == False).order(-Post.startDate).fetch(50)
            posts = Post.query(Post.school_uuid == schoolInfo.uuid, Post.approved == True, Post.endDate >= today).order(-Post.endDate).fetch(50)
            if schoolInfo:
                self.render('school.html', requests=requests, posts=posts, school_uuid = schoolInfo.uuid, school_code = school)
            else:
                self.render("cloud.html", error="You don't belong to that school.")

        else:
            self.render("cloud.html", error="Please login before accessing cloud.")

class Maintain(Handler):
    def get(self):
        user = self.getUserInfo()
        school = self.request.get("s")
        if user['user'] and user['userInfo']:
            schoolInfo = SchoolAccount.getLinkSC(user['userInfo'].user_id, school)
            users = SchoolAccount.query(SchoolAccount.school_uuid == schoolInfo.uuid).fetch()
            usersInfo = []
            for account in users:
                usersInfo.append(Account.query(Account.user_id == account.user_id).fetch(1)[0])
            if users:
                self.render('cloud/maintain.html', users=usersInfo)
        else:
            self.render("cloud.html", error="You don't belong to that school.")

class Send(Handler):
    def post(self):
        data = json.loads(self.request.body)
        postQueryInfo = Post.query(Post.uuid == data['uuid']).fetch()
        post = postQueryInfo[0] if len(postQueryInfo) > 0 else None
        user = self.getUserInfo()
        if verifyLink(user['userInfo'].user_id, post.school_uuid):
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
        user = self.getUserInfo()

        if verifyLink(user['userInfo'].user_id, data['school_uuid']):
            code = str(uuid4())
            invite = Invite(
                uuid = code,
                school_uuid = data['school_uuid'],
                createdBy = user['userInfo'].user_id,
                uses = int(data['numInvites']),
            )
            invite.put()
            self.respondToJson({'code': code})

class Join(Handler):
    def post(self):
        user = self.getUserInfo()
        inviteCode = self.request.get('ic')

        inviteQueryInfo = Invite.query(Invite.uuid == inviteCode).fetch()
        inviteInfo = inviteQueryInfo[0] if len(inviteQueryInfo) > 0 else None

        if inviteInfo and inviteInfo.uses > 0:
            if not verifyLink(user['userInfo'].user_id, inviteInfo.school_uuid):
                schoolAccount = SchoolAccount(
                    user_id = user['userInfo'].user_id,
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
    (static_location + '/maintain', Maintain),
], debug=True)
