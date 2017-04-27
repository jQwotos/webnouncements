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
    # Registers a new user into the database if they don't already exist in the database
    accountQueryInfo = Account.query(Account.user_id == user.user_id()).fetch()
    if len(accountQueryInfo) == 0:
        newAccount = Account(
            name = user.nickname(),
            email = user.email(),
            user_id = user.user_id(),
        )
        newAccount.put()

class Cloud(Handler):
    def get(self):
        # Renders the main page of cloud
        user = users.get_current_user()
        accountQueryInfo = Account.query(Account.user_id == user.user_id()).fetch()
        if len(accountQueryInfo) > 0:
            schools = []
            schools = SchoolAccount.query(SchoolAccount.user_id == user.user_id()).fetch()
            updatedSchools = []
            for school in schools:
                schoolInfo = School.query(School.uuid == school.school_uuid).fetch(1)[0]
                updatedSchools.append({
                    "name": schoolInfo.name,
                    "school_code": schoolInfo.school_code,
                })
            self.render("cloud.html", schools = updatedSchools)
        else:
            registerNewUser(users.get_current_user())
            self.redirect(static_location + '/main')

class GenerateSchool(Handler):
    '''

    The class that is used to generate a school. This is fully implemented HOWEVER hidden and only directly accessible
    the direct link.

    '''
    def get(self):
        self.render("generateSchool.html")

    def post(self):
        user = users.get_current_user()
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
                school_code = school_code.lower(),
            )

            # Automatically make the link between the creator and make them admin of school
            schoolAccount = SchoolAccount(
                user_id = user.user_id(),
                school_uuid = data['uuid'],
                role = "admin"
            )
            schoolAccount.put()
            school.put()
            self.redirect(static_location + "/main")
        else:
            self.render("generateSchool.html", error="School code already taken.", data=data)

app = webapp2.WSGIApplication([
    (static_location + '/main', Cloud),
    (static_location + '/generateSchool', GenerateSchool),
], debug=True)
