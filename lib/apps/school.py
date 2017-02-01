import webapp2, json

from ..supports.main import Handler
from ..supports.tables import Post, SchoolAccount

from google.appengine.ext import ndb
from google.appengine.api import users
from uuid import uuid4

static_location = '/school'

class School(Handler):
    def get(self):
        user = self.getUserInfo()
        school = self.request.get("s")
        if user['user'] and user['userInfo']:
            print("")
            schoolInfo = SchoolAccount.getLinkSC(user['userInfo'].user_id, school)
            requests = Post.query(Post.school_uuid == schoolInfo.uuid, Post.approved == False, Post.denied == False).order(-Post.startDate).fetch(50)
            posts = Post.query(Post.school_uuid == schoolInfo.uuid, Post.approved == True).order(-Post.startDate).fetch(50)
            print("%s|%s" % ('LOOK HERE FOR POST', posts))
            print("%s|%s" % ('LOOK HERE FOR REQUESTS', requests))
            if schoolInfo:
                self.render('school.html', requests=requests, posts=posts)
            else:
                self.render("cloud.html", error="You don't belong to that school.")

        else:
            self.render("cloud.html", error="Please login before accessing cloud.")


app = webapp2.WSGIApplication([
    (static_location + '/main', School),
], debug=True)
