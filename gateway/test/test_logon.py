import requests

def test_logon(alias,email,password):
  logon_url = f"https://z4oiwf4tli.execute-api.eu-west-2.amazonaws.com/{alias}/logon"
  logon_data = {"email":email,"password":password}
  logon_response = requests.post(logon_url, json = logon_data)
  logon_response_body = logon_response.json()
  assert logon_response.status_code == 200
  assert logon_response_body.get("error") == None
  user_id = logon_response_body.get("user_id")
  user_token = logon_response_body.get("user_token")
  assert user_id != None
  assert user_token != None
