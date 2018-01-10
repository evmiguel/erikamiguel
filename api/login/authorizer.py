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
# Constants
#----------------------------------------------------------
DYNAMODB = "dynamodb"

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
        msg = "{}.{}() MUST BE IMPLEMENTED BY A SUBCLASS".format(object.__class__.__name__, "authorize")
        raise NotImplementedError(msg)

###########################################################
# DynamoDB Authorizer Implementation
###########################################################
class DynamoDBSimpleAuthorizer(AbstractAuthorizerAPI):
    '''
        This class is the implementation of a authorizer that
        authorizes basic credentials in DynamoDB.
    '''
    # -----------------------------------------------------
    # Built-in Methods
    # -----------------------------------------------------
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
        :param username: string
        :param password: string
        :return: token string
        '''
        try:
            if self.userCredentialsValid(username, password):
                return self.generateToken()
        except AuthenticationException as e:
            msg = "AuthenticationException: Username or password are invalid! Error {}".format(e)
            logger.error(msg)
            raise AuthenticationException(msg)

    def userCredentialsValid(self, username, password):
        '''
        :param username: string
        :param password: string
        :return: boolean
        '''
        response = self.dynamodb.get_item(
            TableName=self.loginTable,
            Key={'username': {'S': username}}
        )
        status = response['ResponseMetadata']['HTTPStatusCode']
        if 'Item' not in response:  # Item should be in dictionary if the user exists
            msg = "AuthenticationException: User does not exist! HTTP status {}".format(status)
            logger.error(msg)
            raise AuthenticationException(msg)

        # Check if the user matches
        responseUsername = response['Item']['username']['S']
        responsePassword = response['Item']['password']['S']
        return (responseUsername == username and responsePassword == responsePassword and status == 200)


# ----------------------------------------------------------
# Token Validator Classes
# ----------------------------------------------------------
###########################################################
# Abstract Token Validator
###########################################################
class AbstractTokenValidator(object):
    '''
        This class describes the API for
         validating tokens
    '''
    # -----------------------------------------------------
    # Public Methods
    # -----------------------------------------------------
    def validateToken(self, token):
        msg = "{}.{}() MUST BE IMPLEMENTED BY A SUBCLASS".format(object.__class__.__name__, "validateToken")
        raise NotImplementedError(msg)

###########################################################
# DynamoDB Token Validator
###########################################################
class DynamoDBTokenValidator(AbstractTokenValidator):
    '''
        This class is an implementation for a token
        validator against DynamoDB
    '''
    # -----------------------------------------------------
    # Built-in Methods
    # -----------------------------------------------------
    def __init__(self, tokenTable):
        self.tokenTable = tokenTable
        self.dynamodb = boto3.client('dynamodb')

    # -----------------------------------------------------
    # Public Methods
    # -----------------------------------------------------
    def validateToken(self, token):
        logger.info("Validating token {}...".format(token))
        response = self.dynamodb.get_item(
            TableName=self.tokenTable,
            Key={'token': {'S': token}}
        )
        status = response['ResponseMetadata']['HTTPStatusCode']
        if 'Item' not in response or status != 200:  # Item should be in dictionary if the user exists
            msg = "TokenNotFoundException: Token not valid!"
            logger.error(msg)
            raise AuthenticationException(msg)

        return { "tokenValid" : True }

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
    '''
        This is the AWS Authorizer Factory implementation
    '''
    def getAuthorizer(self, type, config):
        if type == DYNAMODB:
            return DynamoDBSimpleAuthorizer(config["dynamoLoginTable"], config["dynamoTokenTable"])

# ----------------------------------------------------------
# Token Validator Factory Classes
# ----------------------------------------------------------
###########################################################
# Abstract Token Validator Factory Interface
###########################################################
class AbstractTokenValidatorFactoryAPI(object):
    '''
        This class describes the methods for creating
        token validator objects in a factory fashion
    '''

    # -----------------------------------------------------
    # Public Methods
    # -----------------------------------------------------
    def createTokenValidator(self, type, config):
        return self.getTokenValidator(type, config)

    def getTokenValidator(self, type, config):
        '''
            Factory method to be implemented for getting
            an authorizer object
        '''
        msg = "{}.{}() MUST BE IMPLEMENTED BY SUBCLASSES".format(object.__class__.__name__, "getTokenValidator")
        raise NotImplementedError(msg)

###########################################################
# AWS Token Validator Factory Interface
###########################################################
class AWSTokenValidatorFactory(AbstractTokenValidatorFactoryAPI):
    '''
        This is the AWS Token Validator Factory
    '''
    def getTokenValidator(self, type, config):
        if type == DYNAMODB:
            return DynamoDBTokenValidator(config["dynamoTokenTable"])

#----------------------------------------------------------
# Custom Exceptions
#----------------------------------------------------------
###########################################################
# Authentication Exception
###########################################################
class AuthenticationException(Exception):
    ''' Raise this for authentication errors '''