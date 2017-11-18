"""
    Author: Erika Miguel

    Unit tests for login modules
"""
import unittest
from login import *

class LoginModulesTests(unittest.TestCase):

    def testCredentialsInstantiation(self):
        credentials = SimpleCredentials("foo", "bar")
        credentialsDictionary = credentials.getCredentials()
        self.assertTrue(credentialsDictionary["credentials"])
        self.assertEquals(credentialsDictionary["credentials"]["username"], "foo")
        self.assertEquals(credentialsDictionary["credentials"]["password"], "bar")