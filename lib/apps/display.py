import datetime
import logging

import webapp2

from google.appengine.ext import ndb

from ..supports.main import Handler
from ..supports.tables import Post, School
from ..supports.constants import time_delta

static_location = '/display'

class Today(Handler):
    def get(self):
        today = datetime.datetime.now().date()
        school = self.request.get('s')
        posts = Post.query(Post.school_uuid == school, Post.approved == True, Post.startDate <= today).fetch()

        schoolQueryInfo = School.query(School.uuid == school).fetch()
        schoolCode = schoolQueryInfo[0].school_code if len(schoolQueryInfo) > 0 else None
        for post in list(posts):
            if not post.endDate >= today:
                posts.remove(post)

        self.renderBlank('display/display.html', posts = posts, school_code=schoolCode)

class Print(Handler):
    def get(self):
        today = datetime.datetime.now().date()
        school = self.request.get('s')
        posts = Post.query(Post.school_uuid == school, Post.approved == True, Post.startDate <= today).fetch()

        schoolQueryInfo = School.query(School.uuid == school).fetch()
        schoolCode = schoolQueryInfo[0].school_code if len(schoolQueryInfo) > 0 else None
        for post in list(posts):
            if not post.endDate >= today:
                posts.remove(post)

        for post in posts:
            if post.readStartDate and post.readEndDate and post.readStartDate <= today and post.readEndDate >= today:
                post.star = True

        self.renderBlank('display/print.html', posts = posts, school_code=schoolCode)

class Read(Handler):
    def get(self):
        today = datetime.datetime.now().date()
        school = self.request.get('s')
        posts = Post.query(Post.school_uuid == school, Post.approved == True).filter(Post.startDate <= today).fetch()
        for post in list(posts):
            if not post.endDate >= today:
                posts.remove(post)

        self.renderBlank('display/read.html', posts = posts)

app = webapp2.WSGIApplication([
    (static_location + '/read', Read),
    (static_location + '/today', Today),
    (static_location + '/print', Print),
], debug=True)
