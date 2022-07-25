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
    "lambdaAlias": "",
    "dataBucket": "",
    "userdataBucket": ""
  },
  "queryStringParameters": {
    "id": "test-id",
    "type": "test-type"
  },
  "body": '{"msg":"hello"}'
}

function_event_load_data = {
  "stageVariables": {
    "lambdaAlias": "",
    "dataBucket": "",
    "userdataBucket": ""
  },
  "queryStringParameters": {
    "id": "test-id",
    "type": "test-type"
  }
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

  function_event_save_data["stageVariables"]["lambdaAlias"] = alias
  function_event_save_data["stageVariables"]["userdataBucket"] = userdataBucket
  function_event_save_data["stageVariables"]["dataBucket"] = dataBucket
  function_event_save_data["queryStringParameters"]["user_id"] = user_id
  function_event_save_data["queryStringParameters"]["user_token"] = user_token
  response = save_data(function_event_save_data, None)
  status_code = response.get('statusCode')
  body = json.loads(response.get('body'))
  error = body.get("error")
  assert status_code == 200 and error == None

  function_event_load_data["stageVariables"]["lambdaAlias"] = alias
  function_event_load_data["stageVariables"]["userdataBucket"] = userdataBucket
  function_event_load_data["stageVariables"]["dataBucket"] = dataBucket
  function_event_load_data["queryStringParameters"]["user_id"] = user_id
  function_event_load_data["queryStringParameters"]["user_token"] = user_token
  response = load_data(function_event_load_data, None)
  status_code = response.get('statusCode')
  body = json.loads(response.get('body'))
  error = body.get("error")
  assert status_code == 200 and error == None
  assert body == {"msg":"hello"}
  