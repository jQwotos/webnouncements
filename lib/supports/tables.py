from google.appengine.ext import ndb
from uuid import uuid4

'''

This is the file in which we store all of the NDB databases

'''

# ndb School Entity
class School(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add = True)
    # A unique identity that can be used to identify a school, this system can and should be replaced using keys on NDB
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

# ndb Relation between Account and School. This is what allows a user to be authenticated to belong to a school
class SchoolAccount(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add = True)
    user_id = ndb.StringProperty(required = True)
    school_uuid = ndb.StringProperty(required = True)
    role = ndb.StringProperty()
    @classmethod
    def getLinkSC(self, request_user, request_sc):
        # Get the information that pertains to the relation between a user and a school code
        linkQueryInfo = self.query(self.user_id == request_user).fetch()
        schoolQueryInfo = School.query(School.school_code == request_sc).fetch()
        schoolInfo = schoolQueryInfo[0] if len(schoolQueryInfo) > 0 else None
        if schoolInfo:
            for link in linkQueryInfo:
                if link.school_uuid == schoolInfo.uuid:
                    return schoolInfo, linkQueryInfo
            return None
        else:
            return None
    @classmethod
    def verifyLink(self, request_user, request_school):
        # Verifies that the user does indeed belong to the school
        return True if len(self.query(SchoolAccount.user_id == request_user, self.school_uuid == request_school).fetch()) > 0 else False


# ndb Post Entity
class Post(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add = True)
    uuid = ndb.StringProperty(required = True)

    # When to display and what to display
    startDate = ndb.DateProperty(required = True)
    endDate = ndb.DateProperty(required = True)
    readStartDate = ndb.DateProperty()
    readEndDate = ndb.DateProperty()
    title = ndb.TextProperty(required = True)
    text = ndb.TextProperty()

    # Approved or Not?
    approved = ndb.BooleanProperty(required = True)
    denied = ndb.BooleanProperty(required = True)
    # The email and name of the person who sent the post request
    submitterEmail = ndb.StringProperty()
    submitterName = ndb.StringProperty()
    # Send an email to this approver to approve, currently not implemented
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
