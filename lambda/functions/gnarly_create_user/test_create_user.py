import json
from gnarly_create_user.source.lambda_function import lambda_handler as create_user

function_event_create_user = {
  "stageVariables": {
  },
  "queryStringParameters": {
  }
}

def call_create_user():
  response = create_user(function_event_create_user, None)
  status_code = response.get('statusCode')
  assert status_code == 200
  responseBody = json.loads(response.get('body'))
  error = responseBody.get("error")
  assert error == None
  return responseBody

def test_create_user(alias,userdataBucket,dataBucket,email,password):
  # error when email missing from request
  function_event_create_user["stageVariables"]["lambdaAlias"] = alias
  function_event_create_user["stageVariables"]["userdataBucket"] = userdataBucket
  function_event_create_user["stageVariables"]["dataBucket"] = dataBucket
  function_event_create_user["body"] = f'{{"password": "{password}"}}'

  response = create_user(function_event_create_user, None)
  status_code = response.get('statusCode')
  body = json.loads(response.get('body'))
  error = body.get("error")
  assert status_code == 200 and error != None

  # error when password missing from request
  function_event_create_user["stageVariables"]["lambdaAlias"] = alias
  function_event_create_user["stageVariables"]["userdataBucket"] = userdataBucket
  function_event_create_user["stageVariables"]["dataBucket"] = dataBucket
  function_event_create_user["body"] = f'{{"email": "{email}"}}'

  response = create_user(function_event_create_user, None)
  status_code = response.get('statusCode')
  body = json.loads(response.get('body'))
  error = body.get("error")
  assert status_code == 200 and error != None

  # success when email and password supplied
  function_event_create_user["stageVariables"]["lambdaAlias"] = alias
  function_event_create_user["stageVariables"]["userdataBucket"] = userdataBucket
  function_event_create_user["stageVariables"]["dataBucket"] = dataBucket
  function_event_create_user["body"] = f'{{"email": "{email}","password": "{password}"}}'

  response = create_user(function_event_create_user, None)
  status_code = response.get('statusCode')
  body = json.loads(response.get('body'))
  error = body.get("error")
  assert status_code == 200 and error == None
