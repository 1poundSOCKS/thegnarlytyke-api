import boto3

client = boto3.client('lambda')

functions = ['gnarly-logon','gnarly-authenticate-user','gnarly-load-data','gnarly-save-data']

for function_name in functions:
  
  alias = client.get_alias(
    FunctionName=function_name,
    Name='test'
  )

  test_function_version = alias["FunctionVersion"]
  
  client.update_alias(
    FunctionName=function_name,
    Name='prod',
    FunctionVersion=test_function_version
  )
