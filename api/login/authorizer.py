"""
    Author: Erika Miguel

    This module contains classes for
    authorizing lambda requests

"""
import boto3, logging, secrets
#----------------------------------------------------------
# Logging Setup
#----------------------------------------------------------
logger = logging.getLogger()

#----------------------------------------------------------
# Authorizer Classes
#----------------------------------------------------------
###########################################################
# Abstract Authorizer Interface
###########################################################
class AbstractAuthorizerAPI(object):
    '''
        This class describes the API for authorizing
        an incoming Lambda request
    '''
    # -----------------------------------------------------
    # Public Methods
    # -----------------------------------------------------
    def authorize(self):
        msg = "{}.{} MUST BE IMPLEMENTED BY A SUBCLASS"
        raise NotImplementedError(msg)

###########################################################
# DynamoDB Authorizer Implementation
###########################################################
class DynamoDBSimpleAuthorizer(AbstractAuthorizerAPI):
    '''
        This class is the implementation of a authorizer that
        authorizes basic credentials in DynamoDB.
    '''
    def __init__(self, table):
        self.table = table

    # -----------------------------------------------------
    # Public Methods
    # -----------------------------------------------------
    def generateToken(self):
        return { 'token' : secrets.token_hex(16) }

    def authorize(self, username, password):
        '''
        :param username:
        :param password:
        :return: token string
        '''
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(self.table)
        response = table.get_item(

            Key={'username': username}
        )
        if response:
            return self.generateToken()
        else:
            msg = "Username or password are invalid!"
            raise AuthenticationException(msg)

#----------------------------------------------------------
# Authorizer Factory Classes
#----------------------------------------------------------
###########################################################
# Abstract Authorizer Factory Interface
###########################################################
class AbstractAuthorizerFactoryAPI(object):
    '''
        This class describes the methods for creating
        authorizer objects in a factory fashion
    '''
    # -----------------------------------------------------
    # Public Methods
    # -----------------------------------------------------
    def createAuthorizer(self, type, config):
        return self.getAuthorizer(type, config)

    def getAuthorizer(self, type, config):
        '''
            Factory method to be implemented for getting
            an authorizer object
        '''
        msg = "{}.{}() MUST BE IMPLEMENTED BY SUBCLASSES".format(object.__class__.__name__, "getAuthorizer")
        raise NotImplementedError(msg)

###########################################################
# AWS Authorizer Interface
###########################################################
class AWSAuthorizerFactory(AbstractAuthorizerFactoryAPI):
    def getAuthorizer(self, type, config):
        if type == "dynamodb":
            return DynamoDBSimpleAuthorizer(config["dynamoLoginTable"])

#----------------------------------------------------------
# Custom Exceptions
#----------------------------------------------------------
###########################################################
# Authentication Exception
###########################################################
class AuthenticationException(Exception):
    ''' Raise this for authentication errors '''