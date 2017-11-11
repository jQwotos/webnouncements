import webapp2

from .src.db import Posting
from .src.main import Handler

static_location = "/supplier"

class Home(Handler):
    def get(self):

class Rented(Handler):
    def post(self):

app = webapp2.WSGIApplication([
    ('%s/home' % static_location, Home),
    ('%s/rented' % static_location, Rented)
])
