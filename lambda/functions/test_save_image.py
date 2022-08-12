import json
import boto3
import uuid
from botocore.errorfactory import ClientError

from gnarly_logon.source.lambda_function import lambda_handler as logon
from gnarly_save_image.source.lambda_function import lambda_handler as save_image

from image_data_sample import image_data

function_event_logon = {
  "stageVariables": {
    "lambdaAlias": "",
    "dataBucket": "",
    "userdataBucket": ""
  }
}

function_event_save_image = {
  "stageVariables": {
    "lambdaAlias": "",
    "dataBucket": "",
    "userdataBucket": ""
  },
  "queryStringParameters": {
    "id": "test-image",
    "type": "test"
  },
  "body": image_data
}

def test_lambda(alias,userdataBucket,dataBucket,email,password):
  function_event_logon["stageVariables"]["lambdaAlias"] = alias
  function_event_logon["stageVariables"]["userdataBucket"] = userdataBucket
  function_event_logon["stageVariables"]["dataBucket"] = dataBucket
  function_event_logon["body"] = f'{{"email": "{email}","password": "{password}"}}'
  response = logon(function_event_logon, None)
  status_code = response.get('statusCode')
  body = json.loads(response.get('body'))
  error = body.get("error")
  assert status_code == 200 and error == None

  user_id = body.get("user_id")
  user_token = body.get("user_token")
  object_id = uuid.uuid4()
  object_type = "test"

  function_event_save_image["stageVariables"]["lambdaAlias"] = alias
  function_event_save_image["stageVariables"]["userdataBucket"] = userdataBucket
  function_event_save_image["stageVariables"]["dataBucket"] = dataBucket
  function_event_save_image["queryStringParameters"]["user_id"] = user_id
  function_event_save_image["queryStringParameters"]["user_token"] = user_token
  function_event_save_image["queryStringParameters"]["id"] = object_id
  function_event_save_image["queryStringParameters"]["type"] = object_type
  response = save_image(function_event_save_image, None)
  status_code = response.get('statusCode')
  body = json.loads(response.get('body'))
  error = body.get("error")
  assert status_code == 200 and error == None
  response_filename = body.get("filename")
  assert response_filename != None

  s3 = boto3.client('s3')
  data_key = "data/images/{}".format(response_filename)
  try:
      s3.get_object(Bucket=dataBucket, Key=data_key)
  except ClientError:
    assert True
