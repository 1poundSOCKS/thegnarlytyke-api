@REM dev
set alias=dev
aws lambda add-permission --function-name "gnarly-logon:%alias%" --source-arn "arn:aws:execute-api:eu-west-2:081277733545:z4oiwf4tli/*/POST/logon" --principal apigateway.amazonaws.com --statement-id allow-api-gateway-%alias% --action lambda:InvokeFunction
@REM aws lambda add-permission --function-name "gnarly-load-data:%alias%" --source-arn "arn:aws:execute-api:eu-west-2:081277733545:z4oiwf4tli/*/GET/load-data" --principal apigateway.amazonaws.com --statement-id allow-api-gateway-%alias% --action lambda:InvokeFunction
@REM aws lambda add-permission --function-name "gnarly-save-data:%alias%" --source-arn "arn:aws:execute-api:eu-west-2:081277733545:z4oiwf4tli/*/POST/save-data" --principal apigateway.amazonaws.com --statement-id allow-api-gateway-%alias% --action lambda:InvokeFunction

@REM test
set alias=test
aws lambda add-permission --function-name "gnarly-logon:%alias%" --source-arn "arn:aws:execute-api:eu-west-2:081277733545:z4oiwf4tli/*/POST/logon" --principal apigateway.amazonaws.com --statement-id allow-api-gateway-%alias% --action lambda:InvokeFunction
@REM aws lambda add-permission --function-name "gnarly-load-data:%alias%" --source-arn "arn:aws:execute-api:eu-west-2:081277733545:z4oiwf4tli/*/GET/load-data" --principal apigateway.amazonaws.com --statement-id allow-api-gateway-%alias% --action lambda:InvokeFunction
@REM aws lambda add-permission --function-name "gnarly-save-data:%alias%" --source-arn "arn:aws:execute-api:eu-west-2:081277733545:z4oiwf4tli/*/POST/save-data" --principal apigateway.amazonaws.com --statement-id allow-api-gateway-%alias% --action lambda:InvokeFunction

@REM prod
set alias=prod
aws lambda add-permission --function-name "gnarly-logon:%alias%" --source-arn "arn:aws:execute-api:eu-west-2:081277733545:z4oiwf4tli/*/POST/logon" --principal apigateway.amazonaws.com --statement-id allow-api-gateway-%alias% --action lambda:InvokeFunction
@REM aws lambda add-permission --function-name "gnarly-load-data:%alias%" --source-arn "arn:aws:execute-api:eu-west-2:081277733545:z4oiwf4tli/*/GET/load-data" --principal apigateway.amazonaws.com --statement-id allow-api-gateway-%alias% --action lambda:InvokeFunction
@REM aws lambda add-permission --function-name "gnarly-save-data:%alias%" --source-arn "arn:aws:execute-api:eu-west-2:081277733545:z4oiwf4tli/*/POST/save-data" --principal apigateway.amazonaws.com --statement-id allow-api-gateway-%alias% --action lambda:InvokeFunction
