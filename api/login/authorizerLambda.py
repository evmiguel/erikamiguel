"""
    Author: Erika Miguel

    This module contains the lambda handler for
    authorizing requests.
"""
import os, json
from authorizer import *

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
# Lambda Handler
#--------------------------------------------------------
def lambda_handler(event, context):
    username = event["username"]
    password = event["password"]

    authFactory = AWSAuthorizerFactory()
    authorizer = authFactory.createAuthorizer("dynamodb", CONFIG)
    return authorizer.authorize(username, password)

if __name__ == '__main__':
    lambda_handler(event={}, context={})