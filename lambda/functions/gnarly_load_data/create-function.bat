set function-name=gnarly-load-data

set scripts_folder=../../scripts
set build_folder=../../build
set output_folder=../../output
set zip_source=%build_folder%/%function-name%

python %scripts_folder%/zip-function2.py function %zip_source%
python %scripts_folder%/create-function2.py %function-name% %zip_source%.zip %output_folder%/%function-name%.role.json %output_folder%/%function-name%.create.json
aws lambda create-alias --function-name %function-name% --name dev --function-version $LATEST > %output_folder%/%function-name%.dev.alias.json
aws lambda publish-version --function-name %function-name% > %output_folder%/%function-name%.function.json
python %scripts_folder%/create-alias.py test %output_folder%/%function-name%.function.json > %output_folder%/%function-name%.test.alias.json
python %scripts_folder%/create-alias.py prod %output_folder%/%function-name%.function.json > %output_folder%/%function-name%.prod.alias.json
