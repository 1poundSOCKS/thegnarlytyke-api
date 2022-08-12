import json
from gnarly_logon.source.lambda_function import lambda_handler as logon
from gnarly_save_data.source.lambda_function import lambda_handler as save_data
from gnarly_load_data.source.lambda_function import lambda_handler as load_data

function_event_logon = {
  "stageVariables": {
    "lambdaAlias": "",
    "dataBucket": "",
    "userdataBucket": ""
  }
}

function_event_save_data = {
  "stageVariables": {
    "dataBucket": "",
    "userdataBucket": ""
  },
  "queryStringParameters": {
  }
}

function_event_load_data = {
  "stageVariables": {
    "dataBucket": "",
    "userdataBucket": ""
  },
  "queryStringParameters": {
  }
}

def call_save_data(id,body,versioned):
  function_event_save_data["queryStringParameters"]["id"] = id
  if versioned != None:
    function_event_save_data["queryStringParameters"]["versioned"] = versioned
  function_event_save_data["body"] = json.dumps(body)
  response = save_data(function_event_save_data, None)
  status_code = response.get('statusCode')
  assert status_code == 200
  responseBody = json.loads(response.get('body'))
  error = responseBody.get("error")
  assert error == None
  return responseBody

def call_load_data(id,versioned):
  function_event_load_data["queryStringParameters"]["id"] = id
  if versioned != None:
    function_event_load_data["queryStringParameters"]["versioned"] = versioned
  response = load_data(function_event_load_data, None)
  status_code = response.get('statusCode')
  responseBody = json.loads(response.get('body'))
  error = responseBody.get("error")
  assert status_code == 200 and error == None
  return responseBody

def test_lambda(alias,userdataBucket,dataBucket,email,password):
  function_event_logon["stageVariables"]["lambdaAlias"] = alias
  function_event_logon["stageVariables"]["userdataBucket"] = userdataBucket
  function_event_logon["stageVariables"]["dataBucket"] = dataBucket
  function_event_logon["body"] = f'{{"email": "{email}","password": "{password}"}}'

  function_event_save_data["stageVariables"]["lambdaAlias"] = alias
  function_event_save_data["stageVariables"]["userdataBucket"] = userdataBucket
  function_event_save_data["stageVariables"]["dataBucket"] = dataBucket

  function_event_load_data["stageVariables"]["lambdaAlias"] = alias
  function_event_load_data["stageVariables"]["userdataBucket"] = userdataBucket
  function_event_load_data["stageVariables"]["dataBucket"] = dataBucket

  response = logon(function_event_logon, None)
  status_code = response.get('statusCode')
  body = json.loads(response.get('body'))
  error = body.get("error")
  assert status_code == 200 and error == None

  user_id = body.get("user_id")
  user_token = body.get("user_token")

  function_event_save_data["queryStringParameters"]["user_id"] = user_id
  function_event_save_data["queryStringParameters"]["user_token"] = user_token

  function_event_load_data["queryStringParameters"]["user_id"] = user_id
  function_event_load_data["queryStringParameters"]["user_token"] = user_token

  # test that non-versioned files always save with the same name and include the user id
  result = call_save_data("test-non-versioned",{"value":"non-versioned content"},'false')
  non_versioned_key = result.get("key")
  non_versioned_filename = result.get("filename")
  assert non_versioned_key == f"test-non-versioned.{user_id}"
  assert non_versioned_filename == f"test-non-versioned.{user_id}.json"

  result = call_load_data("test-non-versioned",'false')
  assert result == {"value":"non-versioned content"}

  result = call_save_data("test-non-versioned",{"value":"non-versioned content update"},'false')
  non_versioned_key = result.get("key")
  non_versioned_filename = result.get("filename")
  assert non_versioned_key == f"test-non-versioned.{user_id}"
  assert non_versioned_filename == f"test-non-versioned.{user_id}.json"

  result = call_load_data("test-non-versioned",'false')
  assert result == {"value":"non-versioned content update"}

  # test that versioned files save with a different name
  result = call_save_data("test-versioned",{"value":"versioned content"},'true')
  versioned_key = result.get("key")
  versioned_filename = result.get("filename")
  assert versioned_key != None
  assert versioned_filename != None

  result = call_save_data("test-versioned",{"value":"versioned content updated"},'true')
  updated_versioned_key = result.get("key")
  updated_versioned_filename = result.get("filename")
  assert updated_versioned_key != None
  assert updated_versioned_filename != None
  assert updated_versioned_key != versioned_filename
  assert updated_versioned_filename != versioned_filename

  result = call_load_data(versioned_key,'true')
  assert result == {"value":"versioned content"}

  result = call_load_data(updated_versioned_key,'true')
  assert result == {"value":"versioned content updated"}
