import webapp2

from ..supports.main import Handler
from ..supports.tables import Account, School, Invite, SchoolAccount

from google.appengine.api import users
from uuid import uuid4

static_location = '/account'

class Login(Handler):
    def get(self):
        self.render('login.html')
        
app = webapp2.WSGIApplication([
    (static_location + '/login', Login),
], debug=True)
