import json
import boto3
from botocore.errorfactory import ClientError

def lambda_handler(event, context):

    USERDATA_BUCKET_NAME = event["bucket"]
    print("userdata bucket: {}".format(USERDATA_BUCKET_NAME))
    
    user_id = event["user_id"]
    user_token = event["user_token"]

    s3 = boto3.client('s3')
    data_key = "active/{}.txt".format(user_token)
    active_user_id = ""
    
    try:
        active_user = s3.get_object(Bucket=USERDATA_BUCKET_NAME, Key=data_key)
        active_user_id = active_user['Body'].read()
        active_user_id = active_user_id.decode('utf-8')
    except ClientError:
        print("user token invalid")

    if active_user_id == "" or user_id != active_user_id:
        return {
            'statusCode': 200,
            'body': json.dumps({"error": "invalid session"})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({})
    }
    