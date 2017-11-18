"""
    Author: Erika Miguel

    Unit tests for login modules
"""
import unittest, os, json
from login.login import *

#--------------------------------------------------------
# Configuration Setup
#--------------------------------------------------------
WORKING_DIR     = os.path.dirname(os.path.realpath(__file__))
__FILEBASENAME__ = os.path.basename(__file__).split('.')[0]
CONFIG_FILENAME = os.path.join("{}".format(WORKING_DIR), "{}.json".format(__FILEBASENAME__))

CONFIG = {}
with open(CONFIG_FILENAME) as f:
        CONFIG = json.load(f)

#--------------------------------------------------------
# Unit Tests
#--------------------------------------------------------
class LoginModulesTests(unittest.TestCase):

    def testCredentialsInstantiation(self):
        credentials = SimpleCredentials("foo", "bar")
        credentialsDictionary = credentials.getCredentials()
        self.assertTrue(credentialsDictionary["credentials"])
        self.assertEquals(credentialsDictionary["credentials"]["username"], "foo")
        self.assertEquals(credentialsDictionary["credentials"]["password"], "bar")

    def testCredentialsAuthentication(self):
        credentials = SimpleCredentials("foo", "bar")
        credentialsAuthenticator = DynamodbCredentialsAuthenticator(credentials, CONFIG)
        self.assertTrue(credentialsAuthenticator.authenticate())