import json
import boto3
# import requests


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    client = boto3.client('dynamodb')

    #dynamodb = boto3.resources('dynamodb')
    #dynamoTable = dynamodb.Table('audit')
    userid = event['queryStringParameters']['user_id']
    username = event['queryStringParameters']['user_name']
    
    ## Print Input
    print(str(userid))
    print(str(username))
    
    data = {}

    data['dynamodb_outcome'] = client.get_item( TableName = 'audit', 
    Key={
        "user_id": {
            'N': userid
        }, 
        "user_name": {
            'S': username
        }        
        }
    )
    data['memory_limit'] = context.memoryLimitMB
    data['function_name'] = context.functionName
    data['RemainingTime'] = context.getRemainingTimeInMillis
    
    
    print(str(data))
    
    # Set the response
    res_body = {}
    res_body['statusCode'] = 200
    res_body['headers'] = {}
    res_body['headers']['Content-Type'] = 'application/json'
    res_body['body'] = json.dumps(data)

    return res_body

    '''
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
    '''
