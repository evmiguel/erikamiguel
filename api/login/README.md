# How-to

## Auth
Create a corresponding config file, authorizerLambda.json, for the Lambda function in the form of:

```
	{
		"dynamoLoginTable": "",
		"dynamoTokenTable": ""
	}
```
where dynamoLoginTable and dynamoTokenTable are names of tables in DynamoDB. Other authorizers can be created as well.

## Unit Tests
```
    cd tests
    python tests.py
```
