import unittest

from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed

from lib.supports import tables

class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_user_stub()

        ndb.get_context().clear_cache()

    def test_creation(self):


    def tearDown(self):
        self.testbed.deactivate()

class UserCreationTest(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_user_stub()
        self.testbed.init_datastore_v3_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def loginUser(self, email = 'bot.jason@jqwotos.com', id='3145', id_admin=False):
        self.testbed.setup_env(
            user_email = email,
            user_id = id,
            user_is_admin = '1' if is_admin else '0',
            overwrite = True)

    def testLogin(self):
        self.assertFalse(users.get_current_user())
        self.loginUser()
        self.assertEquals(users.get_current_user().email(),)
        current_Users = 
