set function-name=gnarly-load-data
set role-name=gnarly-load-data
set policy#1-name=lambda-read-data

aws lambda delete-function --function-name %function-name%
aws iam detach-role-policy --role-name %role-name% --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaRole
aws iam detach-role-policy --role-name %role-name% --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam delete-role-policy --role-name %role-name% --policy-name %policy#1-name%
aws iam delete-role --role-name %role-name%
