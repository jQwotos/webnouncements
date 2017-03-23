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
        # The main page of the school
        user = users.get_current_user()
        school = self.request.get("s")
        # Calls the tables classmethod to get relevent information about a user and a school code
        schoolInfo, linkInfo = SchoolAccount.getLinkSC(user.user_id(), school)

        schoolAccount = linkInfo[0] if len(linkInfo) > 0 else None

        # If the school info does exists then display the page for them
        if schoolInfo:
            self.render('school.html', school_uuid = schoolInfo.uuid, school_code = school, schoolAccount = schoolAccount)
        # Otherwise get mad and throw them back to the main page of cloud
        else:
            logging.warning("User '%s' tried to access '%s' without having permissions." % (user.user_id(), schoolInfo.uuid))
            self.render("cloud.html", error="You don't belong to that school.")

class Send(Handler):
    '''

    Handles the approval and denial of post

    '''
    def post(self):
        user = users.get_current_user()

        data = json.loads(self.request.body)
        postQueryInfo = Post.query(Post.uuid == data['uuid']).fetch()
        post = postQueryInfo[0] if len(postQueryInfo) > 0 else None

        # Makes sure that the user who is trying to modify the post is part of the school
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
    '''

    Generatives invite codes that could be distributed to add more members to the school

    '''
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
    '''

    Handles the user joining a school

    '''
    def add(self, inviteCode):
        # Used to add a user based on invite code
        user = users.get_current_user()
        inviteQueryInfo = Invite.query(Invite.uuid == inviteCode).fetch()
        inviteInfo = inviteQueryInfo[0] if len(inviteQueryInfo) > 0 else None
        # If the invite code exists and has enough uses left then continue
        if inviteInfo and inviteInfo.uses > 0:
            # If the user is not already part of the school then add them!
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
        '''

        Handles the instant invite links

        '''
        # Grab the in URL invite code
        inviteCode = self.request.get('ic')
        # Grabs the users information
        user = users.get_current_user()

        # If the user is signed in then add them to the school
        if user:
            self.add(inviteCode)
        # Otherwise redirect them to login, which will call back this function and retry
        else:
            self.redirect(users.create_login_url('%s/join?ic=%s' % (static_location, inviteCode)))
    def post(self):
        '''

        Handles the post request that is used on the main page of cloud

        '''
        user = users.get_current_user()
        inviteCode = self.request.get('ic')
        self.add(inviteCode)

app = webapp2.WSGIApplication([
    (static_location + '/main', School),
    (static_location  + '/send', Send),
    (static_location + '/generateInvite', GenerateInvite),
    (static_location + '/join', Join),
], debug=True)
