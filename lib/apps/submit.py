import logging

from uuid import uuid4
from datetime import datetime

import webapp2
from google.appengine.ext import ndb


from ..supports.main import Handler
from ..supports.tables import School, Post, SchoolAccount
from ..supports.tabler import verifyLink

static_location = '/submit'
submit_html = "submit.html"

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
                self.render(submit_html, error="Invalid School Code")
        else:
            self.render(submit_html, error="No school code provided")

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
        if error != "":
            self.render(submit_html, data = data, error = error)
        # If no error has occured, then query the for the school and create a post
        else:
            schoolQueryInfo = School.query(School.school_code == data["sc"]).fetch()
            schoolInfo = schoolQueryInfo[0] if len(schoolQueryInfo) > 0 else None
            user = self.getUserInfo()
            approved = False
            submitterName = "Anonymous"
            if user and 'userInfo' in user:
                if verifyLink(user['userInfo'].user_id, schoolInfo.uuid):
                    approved = True
                    submitterName = user['userInfo'].name

            if schoolInfo:
                post = Post(
                    uuid = str(uuid4()),
                    title = data['title'],
                    text = data['text'],
                    startDate = data['startDate'],
                    endDate = data['endDate'],
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
