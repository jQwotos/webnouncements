import webapp2

from .src.db import Posting
from .src.main import Handler

static_location = "/rent"

class Search(Handler):
    def get

app = webapp2.WSGIApplication([
    ('%s/search' % static_location, search)
])
