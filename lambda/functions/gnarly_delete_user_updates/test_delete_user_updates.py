import json
from gnarly_logon.source.lambda_function import lambda_handler as logon
from gnarly_delete_user_updates.source.lambda_function import lambda_handler as delete_user_updates

function_event_logon = {
  "stageVariables": {
    "lambdaAlias": "",
    "dataBucket": "",
    "userdataBucket": ""
  }
}

function_event_publish_user_updates = {
  "stageVariables": {
    "dataBucket": "",
    "userdataBucket": ""
  },
  "queryStringParameters": {
  }
}

def call_delete_user_updates():
  response = delete_user_updates(function_event_publish_user_updates, None)
  status_code = response.get('statusCode')
  assert status_code == 200
  responseBody = json.loads(response.get('body'))
  error = responseBody.get("error")
  assert error == None
  return responseBody

def test_publish_user_updates(alias,userdataBucket,dataBucket,email,password):

  if alias == None:
    alias = 'dev'

  if userdataBucket == None:
    userdataBucket = 'dev.userdata.thegnarlytyke.com'

  if dataBucket == None:
    dataBucket = 'dev.data.thegnarlytyke.com'

  function_event_logon["stageVariables"]["lambdaAlias"] = alias
  function_event_logon["stageVariables"]["userdataBucket"] = userdataBucket
  function_event_logon["stageVariables"]["dataBucket"] = dataBucket
  function_event_logon["body"] = f'{{"email": "{email}","password": "{password}"}}'

  function_event_publish_user_updates["stageVariables"]["lambdaAlias"] = alias
  function_event_publish_user_updates["stageVariables"]["userdataBucket"] = userdataBucket
  function_event_publish_user_updates["stageVariables"]["dataBucket"] = dataBucket

  response = logon(function_event_logon, None)
  status_code = response.get('statusCode')
  body = json.loads(response.get('body'))
  error = body.get("error")
  assert status_code == 200 and error == None

  user_id = body.get("user_id")
  user_token = body.get("user_token")

  function_event_publish_user_updates["queryStringParameters"]["user_id"] = user_id
  function_event_publish_user_updates["queryStringParameters"]["user_token"] = user_token

  responseBody = call_delete_user_updates()
  assert responseBody == {}