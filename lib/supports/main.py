import os
import jinja2
import json

import webapp2

from google.appengine.api import users

from tables import Account

# os.path.dirname(__file__) is the current location of the file
# os.path.join joins the current location with templates
template_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    def respondToJson(self, json_data):
        '''

        Responds to JSON requests with data

        '''
        self.response.out.write(json.dumps((json_data)))

    def write(self, *a, **kw):
        '''

        Basic writing responses with plain text

        '''
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        '''

        Render a template with certain paraments

        '''
        t = jinja_env.get_template(template)
        return t.render(params)

    def renderBlank(self, template, **kw):
        '''

        Render a blank template with parameters
        The difference is mainly just that the navbar does not appear when you renderBlank but
        will in just render.

        '''
        self.write(self.render_str(template, **kw))

    def render(self, template, **kw):
        '''

        Full render, with templating, user management system and paraments.
        This is what is going to be used most of the time.

        '''
        user = users.get_current_user()
        if user:
            self.write(self.render_str(template, user_email = user.email(), logout_url = users.create_logout_url('/account/login'), **kw))
        else:
            self.write(self.render_str(template, login_url = users.create_login_url('/cloud/main'), **kw))
