set scripts-folder=scripts
set source-folder=functions
set build-folder=build
set output-folder=output

set function-name=gnarly-authenticate-user
set folder-name=gnarly_authenticate_user
python %scripts-folder%/zip-function2.py %source-folder%/%folder-name%/function %build-folder%/%function-name%
aws lambda update-function-code --function-name %function-name% --zip-file fileb://%build-folder%/%function-name%.zip --publish > %output-folder%/%function-name%.update.json

set function-name=gnarly-save-data
set folder-name=gnarly_save_data
python %scripts-folder%/zip-function2.py %source-folder%/%folder-name%/function %build-folder%/%function-name%
aws lambda update-function-code --function-name %function-name% --zip-file fileb://%build-folder%/%function-name%.zip --publish > %output-folder%/%function-name%.update.json

set function-name=gnarly-load-data
set folder-name=gnarly_load_data
python %scripts-folder%/zip-function2.py %source-folder%/%folder-name%/function %build-folder%/%function-name%
aws lambda update-function-code --function-name %function-name% --zip-file fileb://%build-folder%/%function-name%.zip --publish > %output-folder%/%function-name%.update.json
