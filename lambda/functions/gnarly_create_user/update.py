import boto3
import shutil

function_name="gnarly-create-user"
zip_folder="../../build"
source_folder="source"

def update_function(function_name):
  client = boto3.client('lambda')

  zip_file = f'{zip_folder}/{function_name}'
  shutil.make_archive(zip_file, 'zip', source_folder)
  zip_file += '.zip'

  with open(zip_file, 'rb') as f:
    zipped_code = f.read()

  client.update_function_code(
    FunctionName=function_name,
    ZipFile=zipped_code,
    Publish=True
  )

update_function(function_name)
