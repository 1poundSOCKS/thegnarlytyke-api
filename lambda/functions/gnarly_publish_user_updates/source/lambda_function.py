import json
import boto3
from botocore.errorfactory import ClientError
import datetime

def authenticate_user(user_id,user_token,lambda_alias,userdata_bucket):
    function_name = "gnarly-authenticate-user:{}".format(lambda_alias)
    print("authenticating with function: {}".format(function_name))
    lambda_client = boto3.client('lambda')
    inputParams = {"user_id": user_id,"user_token":user_token,"bucket":userdata_bucket}
    response = lambda_client.invoke(
        FunctionName = function_name,
        InvocationType = 'RequestResponse',
        Payload = json.dumps(inputParams)
    )
    response = json.load(response['Payload'])
    print(response)

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

    return None
    
def lambda_handler(event, context):

    stage_vars = event['stageVariables']
    lambda_alias = stage_vars["lambdaAlias"]
    userdata_bucket = stage_vars["userdataBucket"]
    data_bucket = stage_vars["dataBucket"]

    print("lambda alias: {}".format(lambda_alias))
    print("userdata bucket: {}".format(userdata_bucket))
    print("data bucket: {}".format(data_bucket))

    parameters = event['queryStringParameters']
    
    user_id = parameters.get('user_id')
    user_token = parameters.get('user_token')

    auth_user_error = authenticate_user(user_id,user_token,lambda_alias,userdata_bucket)
    if auth_user_error != None:
        return auth_user_error

    copy_source = {
        'Bucket': data_bucket,
        'Key': 'data/crag-index.json'
    }

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(data_bucket)

    datetime_stamp = datetime.datetime.now().strftime("%G%m%d.%H%M%S.%f")
    backup_object_id = f'data/crag-index.backup.{user_id}.{datetime_stamp}.json'

    bucket.copy(copy_source, backup_object_id)

    copy_source = {
        'Bucket': data_bucket,
        'Key': f'data/crag-index.{user_id}.json'
    }

    response = {}

    try:
        bucket.copy(copy_source, 'data/crag-index.json')
    except ClientError:
        response = {"success":"no updates to publish"}

    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET"
        },
        'body': json.dumps(response)
    }
