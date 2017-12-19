"""
    Author: Erika Miguel

    This module contains classes for
    authorizing lambda requests

"""
import boto3, logging, secrets, sys, time

#----------------------------------------------------------
# Logging Setup
#----------------------------------------------------------
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

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
    def __init__(self, loginTable, tokenTable, ttl=3600):
        self.loginTable = loginTable
        self.tokenTable = tokenTable
        self.dynamodb = boto3.client('dynamodb')
        self.ttl = ttl

    # -----------------------------------------------------
    # Public Methods
    # -----------------------------------------------------
    def generateToken(self):
        logger.info("Generating token...")
        tokenData = { 'token' : secrets.token_hex(16), 'ttl' : self.ttl, 'createdTime' : int(time.time()), "expireTime" : int(time.time()) + self.ttl }

        logger.info("Adding token {} to database...".format(tokenData['token']))
        response = self.dynamodb.put_item(
            TableName = self.tokenTable,
            Item = { 'token' : {'S' : tokenData['token']},
                     'createdTime': {'N': str(tokenData['createdTime'])},
                     'expireTime' : {'N' : str(tokenData['expireTime'])}
                    }
        )
        status = response["ResponseMetadata"]["HTTPStatusCode"]

        # Raise exception if token cannot be added to DynamoDB
        if status != 200:
            msg = "AuthenticationException: Token failed to generate! Response error {}".format(status)
            raise AuthenticationException(msg)
        return tokenData

    def authorize(self, username, password):
        '''
        :param username:
        :param password:
        :return: token string
        '''
        response = self.dynamodb.get_item(
            TableName = self.loginTable,
            Key={'username': {'S': username} }
        )
        status = response['ResponseMetadata']['HTTPStatusCode']
        if 'Item' not in response:  # Item should be in dictionary if the user exists
            msg = "AuthenticationException: User does not exist!"
            raise AuthenticationException(msg)

        # Check if the user matches
        responseUsername = response['Item']['username']['S']
        responsePassword = response['Item']['password']['S']
        if responseUsername == username and responsePassword == responsePassword and status == 200:
            return self.generateToken()
        else:
            msg = "AuthenticationException: Username or password are invalid! HTTP error {}".format(status)
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
            return DynamoDBSimpleAuthorizer(config["dynamoLoginTable"], config["dynamoTokenTable"])

#----------------------------------------------------------
# Custom Exceptions
#----------------------------------------------------------
###########################################################
# Authentication Exception
###########################################################
class AuthenticationException(Exception):
    ''' Raise this for authentication errors '''