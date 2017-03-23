import logging
import re
from uuid import uuid4

from datetime import datetime, timedelta

from google.appengine.ext import ndb
from google.appengine.api import users


from ..supports.main import Handler
from ..supports.tables import School, Post, SchoolAccount
from ..supports.constants import time_delta, dateTimePattern

static_location = '/submit'
submit_html = "submit/submit.html"
badsubmit_html = "submit/badsubmission.html"

def poster(self, new = True):
    # Retrieve data from form
    data = {
        "sc": self.request.get("sc"),
        "title": self.request.get("title"),
        "text": self.request.get("text"),
        "startDate": datetime.strptime(self.request.get('startDate'), dateTimePattern),
        "endDate": datetime.strptime(self.request.get('endDate'), dateTimePattern),
        "readStartDate": None,
        "readEndDate": None,
    }

    try:
        data['readStartDate'] = datetime.strptime(self.request.get('readStartDate'), dateTimePattern)
        data['readEndDate'] = datetime.strptime(self.request.get('readEndDate'), dateTimePattern)
    except:
        logging.info("No read date was provided for announcement.")

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
            data['startDate'] = data['startDate'] + timedelta(hours=time_delta)
            data['endDate'] = data['endDate'] + timedelta(hours=time_delta)
            if new:
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
                if data['readEndDate'] and data['readStartDate']:
                    post.readStartDate = data['readStartDate']
                    post.readEndDate = data['readEndDate']
                else:
                    logging.info("No read start or end date was provided for post.")
                post.put()
            else:
                postID = self.request.get("pid")
                logging.info("Updating post rather than creating a new one for %s." % (postID))
                postQueryInfo = Post.query(Post.uuid == postID).fetch()
                post = postQueryInfo[0] if len(postQueryInfo) > 0 else None
                logging.info("Post query %s" % (post))
                if post and SchoolAccount.verifyLink(user.user_id(), post.school_uuid):
                    logging.info('The post %s was updated by %s.' % (post.uuid, user.user_id()))
                    post.title = data['title']
                    post.text = data['text']
                    post.startDate = data['startDate']
                    post.endDate = data['endDate']
                    post.readStartDate = data['readStartDate']
                    post.readEndDate = data['readEndDate']

                    post.put()

            if user and approved:
                self.redirect('/school/main?s=%s' % (data['sc']))
            else:
                self.redirect('/')
        else:
            self.render(submit_html, error="Invalid school code", data = data)
