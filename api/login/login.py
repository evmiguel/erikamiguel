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