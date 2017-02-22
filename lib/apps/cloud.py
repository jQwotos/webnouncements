import logging
import json
from uuid import uuid4

import webapp2

from google.appengine.ext import ndb
from google.appengine.api import users

from ..supports.main import Handler
from ..supports.tables import Account, School, Post, SchoolAccount

static_location = '/cloud'

def registerNewUser(user):
    account = Account(
        name = user.nickname(),
        email = user.email(),
        user_id = user.user_id(),
    )

    account.put()

    logging.info("The user account '%s' was created with id '%s'." % (account.name, account.user_id))

# Approve submissions
class Approve(Handler):
    def get(self):
        if not self.userInfo: self.getUserInfo()

        if self.userInfo:
            post = Post.query(Post.school_uuid == userInfo.school_uuid, Post.approved == False, limit=50).fetch()
            self.render('approve.html', post = post)
        else:
            self.render('login.html', error="You are not approved to view this page yet.")

    def post(self):
        data = json.loads(self.request.body)
        postQueryData = Post.query(Post.uuid == data['uuid'])
        post = postQueryData[0] if len(postQueryData) > 0 else None
        logging.info("Post '' was ")
        if post.school_uuid == self.userInfo.school_uuid and post:
            post.denied = True if data['action'] == 'deny' else False
            post.approved = True if data['action'] == 'approve' else False
            post.approvalUUID = self.userInfo.user_id()
            post.approvalEmail = self.userInfo.email()
            post.put()

class Cloud(Handler):
    def get(self):
        user = self.getUserInfo()
        if user['user']:
            if user['user'] and user['userInfo']:
                schools = SchoolAccount.query(SchoolAccount.user_id == user['userInfo'].user_id).fetch()
                updatedSchools = []
                for school in schools:
                    schoolInfo = School.query(School.uuid == school.school_uuid).fetch(1)[0]
                    updatedSchools.append({
                        "name": schoolInfo.name,
                        "school_code": schoolInfo.school_code,
                    })
                self.render("cloud.html", schools = updatedSchools)
            else:
                self.render("cloud.html")
            user = self.getUserInfo()
            if not user['userInfo']:
                registerNewUser(users.get_current_user())
        else:
            self.render("login.html", error="Please login before accessing cloud.")

class GenerateSchool(Handler):
    def get(self):
        if self.getUserInfo(query_database=False):
            self.render("generateSchool.html")
        else:
            self.render("login.html", error="Please login before generating school.")

    def post(self):
        if not self.userInfo: self.getUserInfo()
        if self.userInfo['user']:
            if self.userInfo['userInfo']:
                school_code = self.request.get("sc")
                data = {
                    "uuid": str(uuid4()),
                    "name": self.request.get("name"),
                    "address": self.request.get("address"),
                    "description": self.request.get("description"),
                }
                if len(School.query(School.school_code == school_code).fetch()) == 0:
                    school = School(
                        uuid = data["uuid"],
                        name = data["name"],
                        address = data["address"],
                        description = data['description'],
                        school_code = school_code,
                    )
                    school.put()
                    schoolAccount = SchoolAccount(
                        user_id = self.userInfo['userInfo'].user_id,
                        school_uuid = data['uuid'],
                        role = "admin"
                    )
                    schoolAccount.put()
                    self.redirect(static_location + "/main")
                else:
                    self.render("generateSchool.html", error="School code already taken.", data=data)
            else:
                self.redirect(static_location + '/main')
        else:
            self.render("login.html", error="Please login before generating school.")

app = webapp2.WSGIApplication([
    (static_location + '/approve', Approve),
    (static_location + '/main', Cloud),
    (static_location + '/generateSchool', GenerateSchool),
], debug=True)
