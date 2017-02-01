import webapp2, date

from ..supports.main import Handler
from ..supports.tables import Post

from google.appengine.ext import ndb

static_location = '/display/'

class Display(Handler):
    def get(self):
        school = self.request.get('school')
        template = self.request.get('template')
        date = self.request.get('date')
        Post.query(
            Post.schoolUUID == school,
            Post.startDate <= date if date else 
        ).order(-Post.)


app = webapp2.WSGIApplication([
    (static_location, Display),
], debug=True)
