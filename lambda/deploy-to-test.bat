set function-name=gnarly-authenticate-user
set function-update-output-file=output/%function-name%.update.json

python source/zip-function.py %function-name%
aws lambda update-function-code --function-name %function-name% --zip-file fileb://build/%function-name%.zip --publish > %function-update-output-file%
python source/update-alias.py test %function-update-output-file%

set function-name=gnarly-save-data
set function-update-output-file=output/%function-name%.update.json

python source/zip-function.py %function-name%
aws lambda update-function-code --function-name %function-name% --zip-file fileb://build/%function-name%.zip --publish > output/%function-name%.update.json
python source/update-alias.py test %function-update-output-file%
