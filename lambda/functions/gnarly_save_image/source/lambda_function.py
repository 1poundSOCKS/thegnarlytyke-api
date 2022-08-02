import json
import boto3
import base64
import datetime

STORE_TEXT_DATA = False

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

    parameters = event['queryStringParameters']
    
    user_id = parameters.get('user_id')
    user_token = parameters.get('user_token')

    auth_user_error = authenticate_user(user_id,user_token,lambda_alias,userdata_bucket)
    if auth_user_error != None:
        return auth_user_error

    string = event['body']

    s3 = boto3.client('s3')
    request_data = event['queryStringParameters']
    object_id = request_data['id']
    object_type = request_data['type']

    datetime_stamp = datetime.datetime.now().strftime("%G%m%d.%H%M%S.%f")
    
    split_pos = string.find(',')
    base64_image_data = string[split_pos+1:]
    
    if STORE_TEXT_DATA:
        encoded_data = base64_image_data.encode("utf-8")
        data_key = "images/{}.{}.{}.txt".format(object_id,datetime_stamp,object_type)
        s3.put_object(Bucket=data_bucket, Key=data_key, Body=encoded_data)
    
    binary_image_data = base64.b64decode(base64_image_data)
    filename = "{}.{}.{}.jpg".format(object_id,datetime_stamp,object_type)
    data_key = "images/{}".format(filename)
    s3.put_object(Bucket=data_bucket, Key=data_key, Body=binary_image_data)

    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST"
        },
        'body': json.dumps({"filename":filename})
    }
