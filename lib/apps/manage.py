import json
import datetime
import logging
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
        if not self.userInfo: self.getUserInfo()
        school = self.request.get("sc")
        if self.userInfo['user'] and self.userInfo['userInfo']:
            schoolInfo, linkInfo = SchoolAccount.getLinkSC(self.userInfo['userInfo'].user_id, school)
            users = SchoolAccount.query(SchoolAccount.school_uuid == schoolInfo.uuid).fetch()
            usersInfo = []
            for account in users:
                usersInfo.append(Account.query(Account.user_id == account.user_id).fetch(1)[0])
                usersInfo[-1]['role'] = account.role
            self.render('manage/manage.html', users=usersInfo, school_uuid=schoolInfo.uuid)
        else:
            logging.warning("User '%s' was denied access to /manage because they did not belong to the school." % (self.userInfo['userInfo'].user_id))
            self.render("cloud.html", error="You don't belong to that school.")

class Delete(Handler):
    def post(self):
        if not self.userInfo: self.getUserInfo()
        data = json.loads(self.request.body)

        if self.userInfo['userInfo'] and data['uuid'] and data['school_uuid']:
            schoolAccountQuery = SchoolAccount.query(SchoolAccount.school_uuid == data['school_uuid'], SchoolAccount.user_id == self.userInfo['userInfo'].user_id).fetch()
            if len(schoolAccountQuery) > 0:
                role = schoolAccountQuery[0].role
                if role == "admin":
                    deleteAccountQuery = SchoolAccount.query(SchoolAccount.school_uuid == data['school_uuid'], SchoolAccount.user_id == data['uuid']).fetch(1)
                    if len(deleteAccountQuery) == 1:
                        deleteAccount = deleteAccountQuery[0]
                        deleteAccount.key.delete()
                        logging.info("The user '%s' that belonged to '%s' was deleted by '%s'" % (deleteAccount.user_id, schoolAccountQuery[0].school_uuid, self.userInfo['userInfo'].user_id))
                        self.respondToJson({'success': 'true',
                                            'message': 'The user %s was deleted.' % data['uuid']})
                    else:
                        logging.error("The user '%s' could not be delete because it did not exist in school '%s'" % (data['uuid'], data['school_uuid']))
                        self.respondToJson({'success': 'false', 'message': 'Account not found!'})
                else:
                    logging.warning("The user '%s' has tried to acess management screen for school '%s', howerver they are not admin of school." % (self.userInfo['userInfo'].user_id, schoolAccountQuery[0].school_uuid))
                    self.respondToJson({'success': 'false', 'message': 'Your not an admin for this school!'})
            else:
                logging.warning("The user did not send all data.")
                self.respondToJson({'success': 'false', 'message': "You shouldn't be here."})
app = webapp2.WSGIApplication([
    (static_location + '/main', Manage),
    (static_location + '/delete', Delete)
], debug=True)
