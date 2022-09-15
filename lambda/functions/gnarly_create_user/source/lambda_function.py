import json
from uuid import uuid4
import boto3

def lambda_handler(event, context):

    stage_vars = event['stageVariables']
    lambda_alias = stage_vars["lambdaAlias"]
    userdata_bucket = stage_vars["userdataBucket"]
    data_bucket = stage_vars["dataBucket"]

    print("lambda alias: {}".format(lambda_alias))
    print("userdata bucket: {}".format(userdata_bucket))
    print("data bucket: {}".format(data_bucket))

    users_table_name = f"users.{lambda_alias}"

    print(f"users table: {users_table_name}")

    req_body = event['body']
    req_dict = json.loads(req_body)
    req_email = req_dict.get("email")
    req_pwd = req_dict.get("password")

    response = {}

    if req_email == None or len(req_email) == 0:
        response = {"error":"email missing"}
    elif req_pwd == None or len(req_pwd) == 0:
        response = {"error":"password missing"}
    else:
        response = add_user(users_table_name,req_email,req_pwd)

    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET"
        },
        'body': json.dumps(response)
    }

def add_user(table_name,email,password):
    new_user = {
        "id": uuid4().hex,
        "email": email,
        "password": password,
        "activated": False,
        "root": False
    }

    ddb = boto3.resource('dynamodb')
    users_table = ddb.Table(table_name)
    users_table.put_item(Item=new_user)

    return new_user
