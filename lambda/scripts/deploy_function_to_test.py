import sys
from lambda_helpers import *

if( len(sys.argv) != 4 ):
  print(len(sys.argv))
  print("usage: UpdateFunctionCode <function_name> <zip_source_dir> <temp_dir>")
  sys.exit(1)

try:
  function_name = sys.argv[1]
  function_source_dir = sys.argv[2]
  temp_dir = sys.argv[3]

  updated_function_def = UpdateLambdaFunctionCode(function_name, function_source_dir, temp_dir)
  version = updated_function_def["Version"]
  print(f"Successfully updated (version={version})")

  updated_alias_def = UpdateLambdaFunctionAlias(function_name, "test", version)
  print(updated_alias_def)
  print(f"Alias updated")

except BaseException as err:
  print(f"Failed (error={err})")
  sys.exit(1)
