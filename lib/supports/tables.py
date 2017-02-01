from google.appengine.ext import ndb
from uuid import uuid4

class School(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add = True)
    uuid = ndb.StringProperty(required = True)
    name = ndb.StringProperty(required = True)
    address = ndb.TextProperty(required = True)
    description = ndb.TextProperty(required = True)
    school_code = ndb.StringProperty(required = True)

class Account(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add = True)
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    user_id = ndb.StringProperty(required = True)

class SchoolAccount(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add = True)
    user_id = ndb.StringProperty(required = True)
    school_uuid = ndb.StringProperty(required = True)
    role = ndb.IntegerProperty()
    @classmethod
    def getLinkSC(self, request_user, request_sc):
        linkQueryInfo = self.query(self.user_id == request_user).fetch()
        schoolQueryInfo = School.query(School.school_code == request_sc).fetch()
        schoolInfo = schoolQueryInfo[0] if len(schoolQueryInfo) > 0 else None
        if schoolInfo:
            for link in linkQueryInfo:
                if link.school_uuid == schoolInfo.uuid:
                    return schoolInfo
            return None
        else:
            return None
    @classmethod
    def verifyLink(self, request_user, request_school):
        return True if len(self.query(self.user_id == request_user, self.school_uuid == request_school).fetch()) > 0 else False

class Post(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add = True)
    uuid = ndb.StringProperty(required = True)

    # When to display and what to display
    startDate = ndb.DateProperty()
    endDate = ndb.DateProperty()
    title = ndb.TextProperty()
    text = ndb.TextProperty()

    # Approved or Not?
    approved = ndb.BooleanProperty()
    denied = ndb.BooleanProperty()
    # The email and name of the person who sent the post request
    submitterEmail = ndb.StringProperty()
    submitterName = ndb.StringProperty()
    # Send an email to this approver to approve
    approvalEmail = ndb.StringProperty()
    approverUUID = ndb.StringProperty()
    # School ID that this post belongs to
    school_uuid = ndb.StringProperty()

class Invite(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add = True)
    uuid = ndb.StringProperty(required = True)
    school_uuid = ndb.StringProperty()
    user_id = ndb.StringProperty()
