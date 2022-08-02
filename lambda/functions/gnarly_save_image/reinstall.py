import boto3
import shutil

config_folder="../../config"
zip_folder="../../build"
lambda_role_arn='arn:aws:iam::aws:policy/service-role/AWSLambdaRole'
role_document_file=f"{config_folder}/lambda-default.role.json"

def delete_role(client,role_name,additional_role_policies):
  try:
    client.detach_role_policy(RoleName=role_name,PolicyArn=lambda_role_arn)
  except client.exceptions.NoSuchEntityException:
    pass

  for role_policy_name in additional_role_policies:
    try:
      client.delete_role_policy(RoleName=role_name,PolicyName=role_policy_name)
    except client.exceptions.NoSuchEntityException:
      pass

  try:
    client.delete_role(RoleName=role_name)
  except client.exceptions.NoSuchEntityException:
    pass

def install_role(client,role_name,additional_role_policies):
  with open(role_document_file, 'rb') as f:
    role_document = f.read().decode()

  client = boto3.client('iam')
  role = client.create_role(
    RoleName=role_name,
    AssumeRolePolicyDocument=role_document
  )

  client.attach_role_policy(
    RoleName=role_name,
    PolicyArn=lambda_role_arn
  )

  for role_policy_name in additional_role_policies:
    role_policy_document_file=f'{config_folder}/{role_policy_name}.policy.json'

    with open(role_policy_document_file, 'rb') as f:
      role_policy_document = f.read().decode()

    client.put_role_policy(
      RoleName=role_name,
      PolicyName=role_policy_name,
      PolicyDocument=role_policy_document
    )

  return role

def delete_function(client,function_name):
  try:
    client.delete_function(FunctionName=function_name)
  except client.exceptions.ResourceNotFoundException:
    pass

def install_function(client,function_name,source_folder,role_arn,api_source_arn):
  zip_file = f'{zip_folder}/{function_name}'
  shutil.make_archive(zip_file, 'zip', source_folder)
  zip_file += '.zip'

  with open(zip_file, 'rb') as f:
    zipped_code = f.read()

  published_version = client.create_function(
    FunctionName=function_name,
    Runtime='python3.9',
    Role=role_arn,
    Handler='lambda_function.lambda_handler',
    Code=dict(ZipFile=zipped_code),
    Timeout=30,
    Publish=True
  )

  client.create_alias(
    FunctionName=function_name,
    Name='dev',
    FunctionVersion='$LATEST'
  )

  version = published_version["Version"]

  for alias in ['test','prod']:
    client.create_alias(
        FunctionName=function_name,
        Name=alias,
        FunctionVersion=version
    )

  for alias in ['dev','test','prod']:
    client.add_permission(
      FunctionName=f'{function_name}:{alias}',
      Principal='apigateway.amazonaws.com',
      SourceArn=api_source_arn,
      StatementId='allow-api-gateway',
      Action='lambda:InvokeFunction'
    )

def reinstall(function_name,additional_role_policies,api_source_arn):
  lambda_client = boto3.client('lambda')
  iam_client = boto3.client('iam')

  role_name = function_name

  delete_function(lambda_client,function_name)
  delete_role(iam_client,role_name,additional_role_policies)

  role = install_role(iam_client,role_name,additional_role_policies)
  role_arn = role["Role"]["Arn"]
  install_function(lambda_client,function_name,"source",role_arn,api_source_arn)

reinstall("gnarly-save-image",['lambda-readwrite-data'],'arn:aws:execute-api:eu-west-2:081277733545:z4oiwf4tli/*/POST/save-image')
