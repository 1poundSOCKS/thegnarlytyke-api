import sys
from lambda_helpers import *

def DeployToDev(function_name, function_source_dir):
  print(f'Updating function "{function_name}" with "{function_source_dir}"')
  updated_function_def = UpdateLambdaFunctionCode(function_name, function_source_dir, "../build")
  version = updated_function_def["Version"]
  print(f"Successfully deployed function '{function_name}' (version={version})")

try:
  functions = ['gnarly-logon','gnarly-authenticate-user','gnarly-load-data','gnarly-save-data','gnarly-save-image','gnarly-publish-user-updates']

  for function_name in functions:
    source_folder = function_name
    source_folder = source_folder.replace('-','_')
    source_path = f'../functions/{source_folder}/source'
    DeployToDev(function_name,source_path)

except BaseException as err:
  print(f"Failed (error={err})")
  sys.exit(1)
