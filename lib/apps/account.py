import webapp2

from ..supports.main import Handler
from ..supports.tables import Account, School, Invite, SchoolAccount

from google.appengine.api import users
from uuid import uuid4

static_location = '/account'

class Login(Handler):
    def get(self):
        self.render('login.html')

class Join(Handler):
    def post(self):
        data = json.loads(self.request.body)
        inviteCode = data['inviteCode']

        inviteQueryInfo = Invite.query(Invite.uuid == inviteCode).fetch()
        inviteInfo = inviteQueryInfo if len(inviteQueryInfo) > 0 else None

        if inviteInfo and len(School.query(School.uuid == inviteInfo.school_uuid)) > 0 and inviteInfo.uses >  0:
            currentAddIn = SchoolAccount(
                user_id = user.user_id(),
                school_uuid = inviteInfo.school_uuid(),
            )
            inviteInfo.uses -= 1
            inviteInfo.put()
            currentAddIn.put()

# Old login system
'''
class Register(Handler):
    def get(self):
        self.render("register.html")

    def post(self):
        email = self.request.get("e")

        inviteCode = self.request.get("ic")

        invite = Invite.query(Invite.uuid == inviteCode).fetch()
        schoolUUID = invite['schoolUUID']
        # Check to see if the invite had a pre-registered email address
        if schoolUUID['email']:
            if not email == schoolUUID['email']:


        # Check to see if the user already exists
        if len(Account.query(Account.email == email).fetch()) == 0:
            self.render('register.html', error='Account already exist!')
        else:
            currentuser = Account(
                uuid = str(uuid4()),
                firstName = self.request.get('firstName'),
                lastName = self.request.get('lastName'),
                email = email,
                password = makeSecure(self.requests.get('password')),
            )

            currentuser.put()
            self.redirect(static_location + login)
'''
app = webapp2.WSGIApplication([
    (static_location + '/login', Login),
], debug=True)
