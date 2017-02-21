import json
import datetime
from uuid import uuid4

import webapp2

from google.appengine.ext import ndb
from google.appengine.api import users

from ..supports.main import Handler
from ..supports.tables import Post, SchoolAccount, Invite, School, Account
from ..supports.tabler import verifyLink

static_location = '/manage'

class Manage(Handler):
    def get(self):
        user = self.getUserInfo()
        school = self.request.get("sc")
        if user['user'] and user['userInfo']:
            schoolInfo, linkInfo = SchoolAccount.getLinkSC(user['userInfo'].user_id, school)
            users = SchoolAccount.query(SchoolAccount.school_uuid == schoolInfo.uuid).fetch()
            usersInfo = []
            for account in users:
                usersInfo.append(Account.query(Account.user_id == account.user_id).fetch(1)[0])
            self.render('manage/manage.html', users=usersInfo, school_uuid=schoolInfo.uuid)
        else:
            self.render("cloud.html", error="You don't belong to that school.")

class Delete(Handler):
    def post(self):
        user = self.getUserInfo()
        data = json.loads(self.request.body)

        if user['userInfo'] and data['uuid'] and data['school_uuid']:
            schoolAccountQuery = SchoolAccount.query(SchoolAccount.school_uuid == data['school_uuid'], SchoolAccount.user_id == user['userInfo'].user_id).fetch()
            if len(schoolAccountQuery) > 0:
                role = schoolAccountQuery[0].role
                print("HEY HERE %s" % role)
                if role == "admin":
                    deleteAccountQuery = SchoolAccount.query(SchoolAccount.school_uuid == data['school_uuid'], SchoolAccount.user_id == data['uuid']).fetch(1)
                    if len(deleteAccountQuery) == 1:
                        deleteAccount = deleteAccountQuery[0]
                        deleteAccount.key.delete()
                        self.respondToJson({'success': 'true',
                                            'message': 'The user %s was deleted.' % data['uuid']})
                    else:
                        self.respondToJson({'success': 'false', 'message': 'Account not found!'})
                else:
                    self.respondToJson({'success': 'false', 'message': 'Your not an admin for this school!'})
            else:
                self.respondToJson({'success': 'false', 'message': "You shouldn't be here."})
app = webapp2.WSGIApplication([
    (static_location + '/main', Manage),
    (static_location + '/delete', Delete)
], debug=True)
