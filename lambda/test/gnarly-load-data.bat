set function-name=gnarly-load-data

aws lambda invoke --function-name %function-name% --payload file://payloads/%function-name%.json --cli-binary-format raw-in-base64-out output/%function-name%.invoke.out.json