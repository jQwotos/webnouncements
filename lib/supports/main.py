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
        self.response.out.write(json.dumps((json_data)))

    def getUserInfo(self, query_database=True, result=False):
        user = users.get_current_user()
        if user:
            if query_database:
                userQueryData = Account.query(Account.user_id == user.user_id()).fetch()
                userInfo = userQueryData[0] if len(userQueryData) > 0 else None
                self.userInfo = {'user': user,
                                'userInfo': userInfo}
                if result:
                    return self.userInfo
            else:
                return {'user': user}
        else:
            return {'user': None}

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def renderBlank(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render(self, template, **kw):
        user = users.get_current_user()
        if user:
            self.write(self.render_str(template, user_email = user.email(), logout_url = users.create_logout_url('/account/login'), **kw))
        else:
            self.write(self.render_str(template, login_url = users.create_login_url('/cloud/main'), **kw))
