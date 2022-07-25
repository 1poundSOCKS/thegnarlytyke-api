import os
import requests

def test_gateway(alias,email,password):
  if email == None:
    email = os.environ["GNARLY_TEST_EMAIL"]
  
  if password == None:
    password = os.environ["GNARLY_TEST_PASSWORD"]

  logon_url = f"https://z4oiwf4tli.execute-api.eu-west-2.amazonaws.com/{alias}/logon"
  load_url = f"https://z4oiwf4tli.execute-api.eu-west-2.amazonaws.com/{alias}/load-data"
  save_url = f"https://z4oiwf4tli.execute-api.eu-west-2.amazonaws.com/{alias}/save-data"
  object_id = "dummy-test-file"

  logon_data = {"email":email,"password":password}
  logon_response = requests.post(logon_url, json = logon_data)
  logon_response_body = logon_response.json()
  assert logon_response.status_code == 200
  assert logon_response_body.get("error") == None
  user_id = logon_response_body.get("user_id")
  user_token = logon_response_body.get("user_token")
  assert user_id != None
  assert user_token != None

  save_parameters = f"user_id={user_id}&user_token={user_token}&id={object_id}"
  save_data = {'somekey': 'somevalue'}
  save_response = requests.post(f"{save_url}?{save_parameters}", json = save_data)
  assert save_response.status_code == 200
  save_response_body = save_response.json()
  assert save_response_body.get("error") == None

  load_parameters = f"user_id={user_id}&user_token={user_token}&id={object_id}"
  load_response = requests.get(f"{load_url}?{load_parameters}")
  assert load_response.status_code == 200
  load_response_body = load_response.json()
  assert load_response_body == save_data
