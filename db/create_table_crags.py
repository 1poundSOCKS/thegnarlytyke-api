import boto3

ddb = boto3.resource('dynamodb')

table = ddb.create_table(
    TableName='crags',
    KeySchema=[
        {
            'AttributeName': 'id',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'name',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'id',
            'AttributeType': 'N'
        },
        {
            'AttributeName': 'name',
            'AttributeType': 'S'
        }
    ],
    BillingMode='PAY_PER_REQUEST'
)
