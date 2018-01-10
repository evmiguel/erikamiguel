"""
    Author: Erika Miguel

    Unit tests for login modules
"""
import unittest, os, json, random
import string as str
from login.login import *
from login.authorizer import *

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
        response = credentialsAuthenticator.authenticate()
        self.assertTrue(response)

    def testAuthorizer(self):
        authFactory = AWSAuthorizerFactory()
        authorizer = authFactory.createAuthorizer("dynamodb", CONFIG)
        self.assertTrue(authorizer.loginTable, CONFIG["dynamoLoginTable"])
        self.assertTrue(authorizer.tokenTable, CONFIG["dynamoTokenTable"])

        # A user that exists
        credentials = SimpleCredentials("foo", "bar")
        credentialsDictionary = credentials.getCredentials()["credentials"]
        response = authorizer.authorize(credentialsDictionary["username"], credentialsDictionary["password"])
        self.assertTrue(response["token"])
        self.assertTrue(response["ttl"])
        self.assertTrue(response["createdTime"])
        self.assertTrue(response["expireTime"])

        # A user that does not exist
        credentials = SimpleCredentials("fakeuser", "fakepassword")
        credentialsDictionary = credentials.getCredentials()["credentials"]
        with self.assertRaises(AuthenticationException):
            authorizer.authorize(credentialsDictionary["username"], credentialsDictionary["password"])

    def testTokenValidator(self):
        authFactory = AWSAuthorizerFactory()
        authorizer = authFactory.createAuthorizer("dynamodb", CONFIG)
        credentials = SimpleCredentials("foo", "bar")
        credentialsDictionary = credentials.getCredentials()["credentials"]
        response = authorizer.authorize(credentialsDictionary["username"], credentialsDictionary["password"])

        token = response["token"]
        validator = AWSTokenValidatorFactory().createTokenValidator("dynamodb", CONFIG)
        self.assertTrue(validator.validateToken(token))

        with self.assertRaises(AuthenticationException):
            validator.validateToken(''.join(random.choices(str.ascii_uppercase + str.digits, k=10)))

    def testUserExistsWithAuthorizer(self):
        authorizer = AWSAuthorizerFactory().createAuthorizer("dynamodb", CONFIG)
        credentials = SimpleCredentials("foo", "bar")
        credentialsDictionary = credentials.getCredentials()["credentials"]
        self.assertTrue(authorizer.userCredentialsValid(credentialsDictionary["username"], credentialsDictionary["password"]))


if __name__ == '__main__':
    unittest.main(verbosity=2)

