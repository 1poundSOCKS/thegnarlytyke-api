import shutil
import boto3

def UpdateLambdaFunctionCode(function_name, zip_source, temp_dir):  
  zip_dest = f"{temp_dir}/{function_name}"
  zip_name = f"{zip_dest}.zip"

  print(f"zipping source dir '{zip_source}' to '{zip_name}'")
  shutil.make_archive(zip_dest, 'zip', zip_source)

  print(f"updating code for Lambda function '{function_name}'")

  with open(zip_name, 'rb') as f:
    zipped_code = f.read()

  client=boto3.client("lambda")
  return client.update_function_code(FunctionName=function_name,ZipFile=zipped_code,Publish=True)
  
def UpdateLambdaFunctionAlias(function_name, alias_name, function_version):
  client=boto3.client("lambda")
  return client.update_alias(FunctionName=function_name,Name=alias_name,FunctionVersion=function_version)
