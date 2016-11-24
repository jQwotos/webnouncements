import webapp2, jinja2, os

from google.appengine.ext import ndb

# os.path.dirname(__file__) is the current location of the file
# os.path.join joins the current location with templates
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

# MainPage is a child of Handler, therefore it has all the functions and variables of Handler
class MainPage(Handler):
    def get(self):
        self.render("")

class Login(Handler):
    def get(self):
        self.render("login.html")

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
