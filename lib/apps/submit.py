import logging
#import re

#from uuid import uuid4
#from datetime import datetime, timedelta

import webapp2
from google.appengine.ext import ndb
from google.appengine.api import users

from ..supports.dater import poster
from ..supports.main import Handler
from ..supports.tables import School, Post, SchoolAccount
from ..supports.constants import time_delta

static_location = '/submit'
submit_html = "submit/submit.html"
badsubmit_html = "submit/badsubmission.html"

# Handles submission
class Submit(Handler):
    def get(self):
        # Find the school code from get reqeust in url
        school = self.request.get('sc').lower()
        user = users.get_current_user()

        if not user:
            warning = "Your email account is not registered for access to this application. If you are a [school name] staff member, you can register for access using the instructions provided by your school.  Contact your computer contact teacher if you need more information"
        elif not SchoolAccount.verifyLinkSC(user.user_id(), school):
            warning = '''
            Your email account is not registered for access to this application. If you are a [school name] staff member,
            you can register for access using the instructions provided by your school.  Contact your computer contact 
            teacher if you need more information
            '''
        else:
            warning = ""
        # warning = SchoolAccount.getLinkSC(user.user_id(), school)
        if school:
            schoolQueryInfo = School.query(School.school_code == school).fetch()
            schoolInfo = schoolQueryInfo[0] if len(schoolQueryInfo) > 0 else None

            if schoolInfo:
                # Render template with school_name and school_code prefilled
                self.render(submit_html, data={
                    "sc": school,
                }, school_name = schoolInfo.name, school_code = schoolInfo.school_code, error=warning)
            else:
                self.render(badsubmit_html, error="Invalid School Code")
        else:
            self.render(badsubmit_html, error="No school code provided")

    def post(self):
        # Goto ..supports.dater for more information on poster
        poster(self, new = True)

app = webapp2.WSGIApplication([
    (static_location, Submit),
], debug=True)
