import sys
import shutil

function_name = sys.argv[1]
source_path = "source/{}".format(function_name)
source_build_file = "build/{}".format(function_name)

shutil.make_archive(source_build_file, 'zip', source_path)
