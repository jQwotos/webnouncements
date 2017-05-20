import datetime
import logging

import webapp2

from google.appengine.ext import ndb

from ..supports.main import Handler
from ..supports.tables import Post, School
from ..supports.constants import time_delta

'''

Everything that pertains to displaying, printing, etc... anouncements is in this file.

'''

static_location = '/display'

class Today(Handler):
    def get(self):
        # Get today's announcements based on the school id
        today = datetime.datetime.now().date()
        school = self.request.get('s')
        # Query the database for post that have been approved and that's startdate is <= today
        posts = Post.query(Post.school_uuid == school, Post.approved == True, Post.startDate <= today).fetch()

        schoolQueryInfo = School.query(School.uuid == school).fetch()
        schoolCode = schoolQueryInfo[0].school_code if len(schoolQueryInfo) > 0 else None

        # Remove all of the post that's end date is not >= today
        for post in list(posts):
            if not post.endDate >= today:
                posts.remove(post)

        for post in posts:
            if post.readStartDate and post.readEndDate and post.readEndDate >= today and post.readStartDate <= today:
                post.star = True

        # Simplistic render the posts with school_code
        self.renderBlank('display/display.html', posts = posts, school_code=schoolCode)

class Print(Handler):
    def get(self):
        # Most of this code is duplicated, so it should be moved to a seperate function and that should just be called.
        today = datetime.datetime.now().date()
        school = self.request.get('s')
        posts = Post.query(Post.school_uuid == school, Post.approved == True, Post.readStartDate <= today).fetch()

        schoolQueryInfo = School.query(School.uuid == school).fetch()
        schoolCode = schoolQueryInfo[0].school_code if len(schoolQueryInfo) > 0 else None
        for post in list(posts):
            if post.readEndDate == None or post.readStartDate == None or not post.readEndDate >= today:
                posts.remove(post)

        self.renderBlank('display/print.html', posts = posts, school_code=schoolCode)

app = webapp2.WSGIApplication([
    (static_location + '/today', Today),
    (static_location + '/print', Print),
], debug=True)
