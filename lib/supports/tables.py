from google.appengine.ext import ndb
from uuid import uuid4

# ndb School Entity
class School(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add = True)
    uuid = ndb.StringProperty(required = True)
    name = ndb.StringProperty(required = True)
    address = ndb.TextProperty(required = True)
    description = ndb.TextProperty(required = True)
    school_code = ndb.StringProperty(required = True)

# ndb Personal User Account Entity
class Account(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add = True)
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    user_id = ndb.StringProperty(required = True)

# ndb Relation between Account and School
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

# ndb Post Entity
class Post(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add = True)
    uuid = ndb.StringProperty(required = True)

    # When to display and what to display
    startDate = ndb.DateProperty(required = True)
    endDate = ndb.DateProperty(required = True)
    title = ndb.TextProperty(required = True)
    text = ndb.TextProperty()

    # Approved or Not?
    approved = ndb.BooleanProperty(required = True)
    denied = ndb.BooleanProperty(required = True)
    # The email and name of the person who sent the post request
    submitterEmail = ndb.StringProperty()
    submitterName = ndb.StringProperty()
    # Send an email to this approver to approve
    approvalEmail = ndb.StringProperty()
    approverUUID = ndb.StringProperty()
    # School ID that this post belongs to
    school_uuid = ndb.StringProperty()

# ndb Invite to School Entity
class Invite(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add = True)
    uuid = ndb.StringProperty(required = True)
    createdBy = ndb.StringProperty()
    school_uuid = ndb.StringProperty()
    user_id = ndb.StringProperty()
    uses = ndb.IntegerProperty()
