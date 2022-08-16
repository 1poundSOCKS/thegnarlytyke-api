import boto3
import uuid
import json

from gnarly_logon.source.lambda_function import lambda_handler as logon
from gnarly_save_image.source.lambda_function import lambda_handler as save_image
from gnarly_save_data.source.lambda_function import lambda_handler as save_data
from gnarly_load_data.source.lambda_function import lambda_handler as load_data
from gnarly_publish_user_updates.source.lambda_function import lambda_handler as publish_user_updates

from image_data_sample import image_data

USER_INDEX_OBJECT_ID = 'user-index.json'
CRAG_INDEX_OBJECT_ID = 'data/crag-index.json'
CRAG_INDEX_KEY = 'crag-index'

def call_logon(alias,userdataBucket,email,password):
  function_event_logon = {
    "stageVariables": {
      "lambdaAlias": "",
      "dataBucket": "",
      "userdataBucket": ""
    }
  }

  function_event_logon["stageVariables"]["lambdaAlias"] = alias
  function_event_logon["stageVariables"]["userdataBucket"] = userdataBucket

  function_event_logon["body"] = f'{{"email": "{email}","password": "{password}"}}'
  response = logon(function_event_logon, None)
  status_code = response.get('statusCode')
  body = json.loads(response.get('body'))
  error = body.get("error")
  assert status_code == 200 and error == None
  return body

def call_save_image(alias,userdataBucket,dataBucket,user_id,user_token,id,type):
  function_event_save_image = {
    "stageVariables": {
      "lambdaAlias": "",
      "dataBucket": "",
      "userdataBucket": ""
    },
    "queryStringParameters": {
    }
  }

  function_event_save_image["stageVariables"]["lambdaAlias"] = alias
  function_event_save_image["stageVariables"]["userdataBucket"] = userdataBucket
  function_event_save_image["stageVariables"]["dataBucket"] = dataBucket
  function_event_save_image["queryStringParameters"]["user_id"] = user_id
  function_event_save_image["queryStringParameters"]["user_token"] = user_token
  function_event_save_image["queryStringParameters"]["id"] = id
  function_event_save_image["queryStringParameters"]["type"] = type
  function_event_save_image["body"] = image_data

  response = save_image(function_event_save_image, None)
  status_code = response.get('statusCode')
  body = json.loads(response.get('body'))
  error = body.get("error")
  assert status_code == 200 and error == None
  response_filename = body.get("filename")
  assert response_filename != None
  
  return response_filename

def call_save_data(alias,userdataBucket,dataBucket,user_id,user_token,id,body,versioned):
  function_event_save_data = {
    "stageVariables": {
      "dataBucket": "",
      "userdataBucket": ""
    },
    "queryStringParameters": {
    }
  }

  function_event_save_data["stageVariables"]["lambdaAlias"] = alias
  function_event_save_data["stageVariables"]["userdataBucket"] = userdataBucket
  function_event_save_data["stageVariables"]["dataBucket"] = dataBucket
  function_event_save_data["queryStringParameters"]["user_id"] = user_id
  function_event_save_data["queryStringParameters"]["user_token"] = user_token
  function_event_save_data["queryStringParameters"]["id"] = id

  if versioned == True:
    function_event_save_data["queryStringParameters"]["versioned"] = 'true'
  else:
    function_event_save_data["queryStringParameters"]["versioned"] = 'false'
  
  function_event_save_data["body"] = body
  response = save_data(function_event_save_data, None)
  status_code = response.get('statusCode')
  assert status_code == 200
  responseBody = json.loads(response.get('body'))
  error = responseBody.get("error")
  assert error == None
  return responseBody

def call_load_data(alias,userdataBucket,dataBucket,user_id,user_token,id,versioned):
  function_event_load_data = {
    "stageVariables": {
      "dataBucket": "",
      "userdataBucket": ""
    },
    "queryStringParameters": {
    }
  }

  function_event_load_data["stageVariables"]["lambdaAlias"] = alias
  function_event_load_data["stageVariables"]["userdataBucket"] = userdataBucket
  function_event_load_data["stageVariables"]["dataBucket"] = dataBucket
  function_event_load_data["queryStringParameters"]["user_id"] = user_id
  function_event_load_data["queryStringParameters"]["user_token"] = user_token
  function_event_load_data["queryStringParameters"]["id"] = id

  if versioned == True:
    function_event_load_data["queryStringParameters"]["versioned"] = 'true'
  else:
    function_event_load_data["queryStringParameters"]["versioned"] = 'false'

  response = load_data(function_event_load_data, None)
  status_code = response.get('statusCode')
  responseBody = json.loads(response.get('body'))
  error = responseBody.get("error")
  assert status_code == 200 and error == None
  return responseBody

def call_publish_user_updates(alias,userdataBucket,dataBucket,user_id,user_token):
  function_event_publish_user_updates = {
    "stageVariables": {
      "dataBucket": "",
      "userdataBucket": ""
    },
    "queryStringParameters": {
    }
  }

  function_event_publish_user_updates["stageVariables"]["lambdaAlias"] = alias
  function_event_publish_user_updates["stageVariables"]["userdataBucket"] = userdataBucket
  function_event_publish_user_updates["stageVariables"]["dataBucket"] = dataBucket
  function_event_publish_user_updates["queryStringParameters"]["user_id"] = user_id
  function_event_publish_user_updates["queryStringParameters"]["user_token"] = user_token

  response = publish_user_updates(function_event_publish_user_updates, None)
  status_code = response.get('statusCode')
  assert status_code == 200
  responseBody = json.loads(response.get('body'))
  error = responseBody.get("error")
  assert error == None
  return responseBody

def test_lambda(alias,userdataBucket,dataBucket,email,password):

  # clear the userdata bucket
  s3 = boto3.resource('s3')
  s3_userdata_bucket = s3.Bucket(userdataBucket)
  s3_userdata_bucket.objects.delete()

  # clear the data bucket
  s3 = boto3.resource('s3')
  s3_data_bucket = s3.Bucket(dataBucket)
  s3_data_bucket.objects.delete()

  # create a user
  s3_client = boto3.client('s3')
  user_id = str(uuid.uuid4())
  user_record = f'{{"email": "{email}","id": "{user_id}","password": "{password}"}}'
  user_index_data = f'{{"users": [{user_record}]}}'
  s3_client.put_object(Bucket=userdataBucket,Key=USER_INDEX_OBJECT_ID,Body=user_index_data)

  # create a skelton crag index
  crag_index_data = '{}'
  s3_client.put_object(Bucket=dataBucket,Key=f'{CRAG_INDEX_OBJECT_ID}',Body=crag_index_data)

  # logon
  logon_response = call_logon(alias,userdataBucket,email,password)
  user_id = logon_response.get("user_id")
  user_token = logon_response.get("user_token")

  # define a crag id for the tests
  crag_id = str(uuid.uuid4())

  image_save_file = call_save_image(alias,userdataBucket,dataBucket,user_id,user_token,crag_id,'crag')

  # save a crag
  crag_name = 'Baildon Bank'
  crag_key = f'{crag_id}.crag'
  crag_data = f'{{"id":"{crag_id}","name":"{crag_name}"}}'
  crag_save_response = call_save_data(alias,userdataBucket,dataBucket,user_id,user_token,crag_key,crag_data,True)
  crag_load_key = crag_save_response.get("key")

  # save an updated crag index
  crag_index_record = f'{{"id": "{crag_id}","name": "{crag_name}","cragKey":"{crag_load_key}","imageFile":"{image_save_file}"}}'
  crag_index_data = f'{{"crags": [{crag_index_record}]}}'
  call_save_data(alias,userdataBucket,dataBucket,user_id,user_token,CRAG_INDEX_KEY,crag_index_data,False)

  # load the crag index
  load_crag_index_data = call_load_data(alias,userdataBucket,dataBucket,user_id,user_token,CRAG_INDEX_KEY,False)
  crags = load_crag_index_data.get("crags")
  assert len(crags) == 1
  assert crags[0].get("id") == crag_id
  assert crags[0].get("name") == crag_name

  # extract the key from the index record to load the crag data
  load_crag_key = crags[0].get("cragKey")

  # load the crag
  load_crag_data = call_load_data(alias,userdataBucket,dataBucket,user_id,user_token,load_crag_key,True)
  assert load_crag_data.get("id") == crag_id
  assert load_crag_data.get("name") == crag_name

  # publish the user updates
  call_publish_user_updates(alias,userdataBucket,dataBucket,user_id,user_token)
  