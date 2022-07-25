import sys
import json
import boto3

function_name = sys.argv[1]
role_details_file = sys.argv[2]

source_build_file = "build/{}".format(function_name)
source_build_zipfile = "{}.zip".format(source_build_file)

with open(source_build_zipfile, 'rb') as f:
	zipped_code = f.read()

with open(role_details_file, 'r') as f:
	role_details = f.read()

role_details_obj = json.loads(role_details)

role_arn = role_details_obj["Role"]["Arn"]

client = boto3.client('lambda')

response = client.create_function(
    FunctionName=function_name,
    Runtime='python3.9',
    Role=role_arn,
    Handler='lambda_function.lambda_handler',
    Code=dict(ZipFile=zipped_code),
    Timeout=10
)

responseText = json.dumps(response, indent=2)

log_file = 'output/{}.create.json'.format(function_name)

with open(log_file, 'w') as f:
	f.write(responseText)
