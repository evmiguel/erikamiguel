"""
    Author: Erika Miguel

    This module validates tokens in the
    DynamoDb table
"""
import os, json, logging
from authorizer import *
#----------------------------------------------------------
# Logging Setup
#----------------------------------------------------------
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#--------------------------------------------------------
# Configuration Setup
#--------------------------------------------------------
WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
__FILEBASENAME__ = os.path.basename(__file__).split('.')[0]
CONFIG_FILENAME = os.path.join("{}".format(WORKING_DIR), "{}.json".format(__FILEBASENAME__))

CONFIG = {}
with open(CONFIG_FILENAME) as f:
    CONFIG = json.load(f)

#--------------------------------------------------------
# Constants
#--------------------------------------------------------
ALLOW   = "Allow"
DENY    = "Deny"
UNAUTHORIZED = "Unauthorized"

def generatePolicy(resource, effect=DENY):
    # -------------------------------------
    # Auth Response
    # -------------------------------------
    authResponse = {}
    authResponse["principalId"] = "*"

    # -------------------------------------
    # Policy Document
    # -------------------------------------
    policyDocument = {}
    policyDocument["Version"] = '2012-10-17'  # default version
    policyDocument["Statement"] = []

    #-------------------------------------
    # Policy Statement
    #-------------------------------------
    statementOne = {}
    statementOne["Action"] = 'execute-api:Invoke'  # default action
    statementOne["Effect"] = effect
    statementOne["Resource"] = resource
    policyDocument["Statement"].append(statementOne)

    authResponse["policyDocument"] = policyDocument
    return authResponse

#--------------------------------------------------------
# Lambda Handler
#--------------------------------------------------------
def lambda_handler(event, context):
    # -------------------------------------
    # Extract API Resources from methodArn string
    # -------------------------------------
    arnResources = event["methodArn"].split(':') # form ['arn', 'aws', 'execute-api', 'us-east-1', 'ACCT_HUM', 'API_ID/null/GET/']
    apiGatewayPath = arnResources[5].split('/')
    resource = '/'  #root resource
    # Extract the rest of the URI if there is more to the path
    if apiGatewayPath[3]:
        resource += apiGatewayPath[3]

    # -------------------------------------
    # Extract Headers
    # -------------------------------------
    headers = event["headers"]
    username = headers["Username"]
    password = headers["Password"]
    token = headers["Token"]

    # -------------------------------------
    # Validate User Credentials
    # -------------------------------------
    authFactory = AWSAuthorizerFactory()
    authorizer = authFactory.createAuthorizer("dynamodb", CONFIG)

    # Deny authorization if credentials are invalid
    try:
        credsValid = authorizer.userCredentialsValid(username, password)
        logger.info("Credentials valid: {}".format(credsValid))
        tokenFactory = AWSTokenValidatorFactory()
        tokenValidator = tokenFactory.createTokenValidator("dynamodb", CONFIG)
        tokenValid = tokenValidator.validateToken(token)
        logger.info("Token valid: {}".format(tokenValid))
        effect = ALLOW if tokenValid and credsValid else DENY
        authResponse = generatePolicy(resource, effect)
        return authResponse
    except AuthenticationException as e:
        logger.error("Credentials invalid! With error {}".format(e))
        raise Exception("Unauthorized: Credentials or token are invalid!")
