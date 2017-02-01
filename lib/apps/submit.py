import webapp2
from uuid import uuid4
from datetime import datetime

from ..supports.main import Handler
from ..supports.tables import School, Post

from google.appengine.ext import ndb

static_location = '/submit'
submit_html = "submit.html"

# Approve submissions

class Submit(Handler):
    def get(self):
        school = self.request.get('sc')

        if school:
            schoolQueryInfo = School.query(School.school_code == school).fetch()
            schoolInfo = schoolQueryInfo[0] if len(schoolQueryInfo) > 0 else None

            if schoolInfo:
                self.render(submit_html, data={
                    "sc": school,
                }, school_name = schoolInfo.name, school_code = schoolInfo.school_code)
            else:
                self.render(submit_html, error="Invalid School Code")
        else:
            self.render(submit_html, error="No school code provided")

    def post(self):
        data = {
            "sc": self.request.get("sc"),
            "title": self.request.get("title"),
            "text": self.request.get("text"),
            "startDate": datetime.strptime(self.request.get("startDate"), '%d %B, %Y'),
            "endDate": datetime.strptime(self.request.get("endDate"), '%d %B, %Y'),
        }

        error = ""
        for item in data:
            if data[item] == "":
                error += ("Please fill out %s\n" % (item))
        if error != "":
            self.render(submit_html, data = data, error = error)
        else:
            schoolQueryInfo = School.query(School.school_code == data["sc"]).fetch()
            schoolInfo = schoolQueryInfo[0] if len(schoolQueryInfo) > 0 else None

            if schoolInfo:
                post = Post(
                    uuid = str(uuid4),
                    title = data['title'],
                    text = data['text'],
                    startDate = data['startDate'],
                    endDate = data['endDate'],
                    school_uuid = schoolInfo.uuid,
                )
                post.put()
                self.redirect('/')
            else:
                self.render(submit_html, error="Invalid school code", data = data)

app = webapp2.WSGIApplication([
    (static_location, Submit),
], debug=True)
