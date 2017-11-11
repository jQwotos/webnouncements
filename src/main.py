import os
import json

import webapp2


class Handler(webapp2.RequestHandler):
    def respond(self, json_data):
        self.response.out.write(json.dumps((json_data)))
        
