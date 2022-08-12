import json
import boto3
from botocore.errorfactory import ClientError

def lambda_handler(event, context):

    stage_vars = event['stageVariables']
    LAMBDA_ALIAS = stage_vars["lambdaAlias"]
    DATA_BUCKET_NAME = stage_vars["dataBucket"]
    USERDATA_BUCKET_NAME = stage_vars["userdataBucket"]

    print("lambda alias: {}".format(LAMBDA_ALIAS))
    print("data bucket: {}".format(DATA_BUCKET_NAME))
    print("userdata bucket: {}".format(USERDATA_BUCKET_NAME))

    parameters = event['queryStringParameters']
    
    user_id = parameters.get('user_id')
    user_token = parameters.get('user_token')

    # check authentication
    function_name = "gnarly-authenticate-user:{}".format(LAMBDA_ALIAS)
    print("authenticating with function: {}".format(function_name))
    lambda_client = boto3.client('lambda')
    inputParams = {"user_id": user_id,"user_token":user_token,"bucket":USERDATA_BUCKET_NAME}
    response = lambda_client.invoke(
        FunctionName = function_name,
        InvocationType = 'RequestResponse',
        Payload = json.dumps(inputParams)
    )
    response = json.load(response['Payload'])
    print("authentication response: {}".format(response))

    if response["statusCode"] == 200:
        body = response["body"]
        bodyObj = json.loads(body)
        authError = bodyObj.get("error")

    if response["statusCode"] != 200 or authError:
        return {
            "statusCode": 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST'
            },
            "body": json.dumps(
                {
                    "error": "not authorised"
                }
            )
        }
    
    s3 = boto3.client('s3')
    object_id = parameters['id']
    versioned = parameters['versioned']

    default_key = f"{object_id}"
    default_filename = f"{default_key}.json"
    default_data_key = f"data/{default_filename}"

    key = f"{object_id}.{user_id}"
    filename = f"{key}.json"
    data_key = f"data/{filename}"
    
    object = None

    if versioned == 'false':
        try:
            object = s3.get_object(Bucket=DATA_BUCKET_NAME, Key=data_key)
        except ClientError:
            object = None

    if object == None:
        try:
            object = s3.get_object(Bucket=DATA_BUCKET_NAME, Key=default_data_key)
        except ClientError:
            return {
                "statusCode": 200,
                'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST'
                },
                "body": json.dumps(
                    {
                        "error": "data with key '{}' does not exist".format(default_filename)
                    }
                )
            }

    object_data = object['Body'].read()
    return_data = object_data.decode()

    return {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST'
        },
        "body": return_data
    }
