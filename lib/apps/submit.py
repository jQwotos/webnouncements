import logging

from uuid import uuid4
from datetime import datetime, timedelta

import webapp2
from google.appengine.ext import ndb
from google.appengine.api import users


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
        school = self.request.get('sc')

        if school:
            schoolQueryInfo = School.query(School.school_code == school).fetch()
            schoolInfo = schoolQueryInfo[0] if len(schoolQueryInfo) > 0 else None

            if schoolInfo:
                # Render template with school_name and school_code prefilled
                self.render(submit_html, data={
                    "sc": school,
                }, school_name = schoolInfo.name, school_code = schoolInfo.school_code)
            else:
                self.render(badsubmit_html, error="Invalid School Code")
        else:
            self.render(badsubmit_html, error="No school code provided")

    def post(self):
        # Retrieve data from form
        data = {
            "sc": self.request.get("sc"),
            "title": self.request.get("title"),
            "text": self.request.get("text"),
            "startDate": datetime.strptime(self.request.get("startDate"), '%d %B, %Y'),
            "endDate": datetime.strptime(self.request.get("endDate"), '%d %B, %Y'),
        }

        # Check if any fields were blank
        error = ""
        for item in data:
            if data[item] == "":
                error += ("Please fill out %s\n" % (item))

        schoolQueryInfo = School.query(School.school_code == data["sc"]).fetch()
        schoolInfo = schoolQueryInfo[0] if len(schoolQueryInfo) > 0 else None

        if not schoolInfo:
            error += "Invalid school code \n"

        if error != "":
            self.render(submit_html, data = data, error = error)
        # If no error has occured, then query the for the school and create a post
        else:
            user = users.get_current_user()
            approved = False
            submitterName = "Anonymous"
            if user:
                if SchoolAccount.verifyLink(user.user_id(), schoolInfo.uuid):
                    approved = True
                    submitterName = user.nickname()

            if schoolInfo:
                post = Post(
                    uuid = str(uuid4()),
                    title = data['title'],
                    text = data['text'],
                    startDate = data['startDate'] + timedelta(hours=time_delta),
                    endDate = data['endDate'] + timedelta(hours=time_delta),
                    school_uuid = schoolInfo.uuid,
                    approved = approved,
                    denied = False,
                    submitterName = submitterName,
                )
                post.put()
                self.redirect('/')
            else:
                self.render(submit_html, error="Invalid school code", data = data)

app = webapp2.WSGIApplication([
    (static_location, Submit),
], debug=True)
