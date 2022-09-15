import boto3

ddb = boto3.resource('dynamodb')

def create_table_users(env):
  table = ddb.create_table(
      TableName=f'users.{env}',
      KeySchema=[
          {
              'AttributeName': 'id',
              'KeyType': 'HASH'
          },
          {
              'AttributeName': 'email',
              'KeyType': 'RANGE'
          }
      ],
      AttributeDefinitions=[
          {
              'AttributeName': 'id',
              'AttributeType': 'S'
          },
          {
              'AttributeName': 'email',
              'AttributeType': 'S'
          }
      ],
      BillingMode='PAY_PER_REQUEST'
  )

create_table_users('dev')
create_table_users('test')
create_table_users('prod')
