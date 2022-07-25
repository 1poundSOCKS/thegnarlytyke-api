import sys
import json
import boto3

alias_name = sys.argv[1]
function_details_file = sys.argv[2]

with open(function_details_file, 'r') as f:
	function_details = f.read()

function_details_obj = json.loads(function_details)

function_name = function_details_obj["FunctionName"]
version = function_details_obj["Version"]

client = boto3.client('lambda')

response = client.update_alias(
    FunctionName=function_name,
    Name=alias_name,
    FunctionVersion=version
)

responseText = json.dumps(response, indent=2)

print(responseText)
