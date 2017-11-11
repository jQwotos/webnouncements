import logging

from google.appengine.ext import ndb
from uuid import uuid4

class Game(ndb.Model):
    uuid = ndb.StringProperty(required = True)
    

class Posting(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add = True)


class Genre(ndb.Model):


class User(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add = True)
