aws lambda invoke --function-name arn:aws:lambda:eu-west-2:081277733545:function:AuthenticateUser --payload file://payloads/authenticate-user.json --cli-binary-format raw-in-base64-out output/lambda.out.json