"""
    Author: Erika Miguel

    This module defines a login flow for AWS Lambda
"""
#----------------------------------------------------------
# Credentials Classes
#----------------------------------------------------------
###########################################################
# Abstract Credentials Interface
###########################################################
class AbstractCredentialsAPI(object):
    '''
        This class describes the methods that a credentials
        object should implement
    '''
    def getCredentials(self):
        msg = "{}.{} MUST BE IMPLEMENTED BY A SUBCLASS".format(object.__class__.__name__, "getCredentials")
        raise NotImplementedError(msg)

###########################################################
# Simple Credentials Object
###########################################################
class SimpleCredentials(AbstractCredentialsAPI):
    '''
        This class describes a simple credentials object
    '''
    # -----------------------------------------------------
    # Private Methods
    # -----------------------------------------------------
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.credentials = {}

    def __getCredentialsObject(self):
        if not self.credentials:
            self.credentials = { "credentials" : { "username" : self.username, "password" : self.password } }
        return self.credentials
    # -----------------------------------------------------
    # Public Methods
    # -----------------------------------------------------
    def getCredentials(self):
        return self.__getCredentialsObject()

#----------------------------------------------------------
# Credentials Validator Classes
#----------------------------------------------------------
###########################################################
# Abstract Credentials Validator Interface
###########################################################
class AbstractCredentialsAuthenticatorAPI(object):
    '''
        This class describes the methods that a credentials
        validator should implement.

        A credentials authenticator should interact with a login
        API to return an object that can be passed with an
        HTTP API call
    '''


    def authenticate(self):
        msg = "{}.{} MUST BE IMPLEMENTED BY A SUBCLASS".format(object.__class__.__name__, "authenticate")
        raise NotImplementedError(msg)

###########################################################
# Simple Credentials Validator Interface
###########################################################
class DynamodbCredentialsAuthenticator(AbstractCredentialsAuthenticatorAPI):
    '''
        This is a dynamodb authenticator implementation.
        It expects a SimpleCredentials object for initialization
    '''
    # -----------------------------------------------------
    # Private Methods
    # -----------------------------------------------------
    def __init__(self, credentialsObject, config):
        self.credentialsObject = credentialsObject
        self.config = config

    # -----------------------------------------------------
    # Public Methods
    # -----------------------------------------------------
    def authenticate(self):
        credentialsDict = self.credentialsObject.getCredentials()
        credentials = credentialsDict["credentials"]
        #TODO send credentials to auth endpoint