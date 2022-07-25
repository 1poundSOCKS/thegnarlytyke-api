import json
import boto3
import uuid
# import bcrypt

def lambda_handler(event, context):
    
    stage_vars = event['stageVariables']
    LAMBDA_ALIAS = stage_vars["lambdaAlias"]
    USERDATA_BUCKET_NAME = stage_vars["userdataBucket"]

    print("lambda alias: {}".format(LAMBDA_ALIAS))
    print("userdata bucket: {}".format(USERDATA_BUCKET_NAME))

    body_data = event['body']
    body_object = json.loads(body_data)
    email = body_object['email']
    password = body_object['password']
    print(f"email: {email}")
    print(f"password: {password}")

    # bytePwd = password.encode()
    # mySalt = bcrypt.gensalt()
    # hashPwd = bcrypt.hashpw(bytePwd, mySalt)
    
    # hash = "$2b$12$U6YOPf4rM2H52t1TKzS/GO0WKmHs3MAfZlfcQQiyK7vsx/qKqiwdu"
    # hashBytes = hash.encode()
    #  and bcrypt.checkpw(bytePwd, hashBytes)

    # load the user index
    s3 = boto3.client('s3')
    data_key = "user-index.json"
    user_index_read = s3.get_object(Bucket=USERDATA_BUCKET_NAME, Key=data_key)
    user_index_data = user_index_read['Body'].read()
    user_index = json.loads(user_index_data)
    
    # check the user exists
    user_exists = False
    password_matches = False
    user_id = ""
    for index, item in enumerate(user_index["users"]):
        if item["email"] == email:
            user_exists = True
            user_id = item["id"]
            if item["password"] == password:
                password_matches = True

    # fail if the user doesn't exist
    if user_exists == False:
        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST"
            },
            'body': json.dumps({"error": "user does not exist"})
        }

    # fail if the password doesn't match
    if password_matches == False:
        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST"
            },
            'body': json.dumps({"error": "invalid password"})
        }

    user_token = uuid.uuid4()
    user_logon_data_key = "active/{}.txt".format(user_token)
    
    s3 = boto3.client('s3')
    s3.put_object(Bucket=USERDATA_BUCKET_NAME, Key=user_logon_data_key, Body=user_id)

    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST"
        },
        'body': json.dumps({"user_id":user_id,"user_token":str(user_token)})
    }

def GetStage(event):
    request_context = event["requestContext"]
    return request_context["stage"]