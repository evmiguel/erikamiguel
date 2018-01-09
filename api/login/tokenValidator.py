"""
    Author: Erika Miguel

    This module validates tokens in the
    DynamoDb table
"""
#--------------------------------------------------------
# Constants
#--------------------------------------------------------
ALLOW   = "allow"
DENY    = "deny"

def generatePolicy(resource, effect=DENY):
    authResponse = {}
    authResponse["principalId"] = "*"
    policyDocument = {}
    policyDocument["Version"] = '2012-10-17'  # default version
    policyDocument["Statement"] = []
    statementOne = {}
    statementOne["Action"] = 'execute-api:Invoke'  # default action
    statementOne["Effect"] = effect
    statementOne["Resource"] = resource
    policyDocument["Statement"].append(statementOne)
    authResponse["policyDocument"] = policyDocument

#--------------------------------------------------------
# Lambda Handler
#--------------------------------------------------------
def lambda_handler(event, context):
    arnResources = event["methodArn"].split(':') # form ['arn', 'aws', 'execute-api', 'us-east-1', 'ACCT_HUM', 'API_ID/null/GET/']
    apiGatewayPath = arnResources[5].split('/')
    resource = '/'  #root resource
    # Extract the rest of the URI if there is more to the path
    if apiGatewayPath[3]:
        resource += apiGatewayPath[3]



    effect = "Allow"
    authResponse = generatePolicy(resource, effect)

    return authResponse
