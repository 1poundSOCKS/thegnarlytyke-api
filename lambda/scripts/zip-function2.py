import sys
import shutil

zip_source = sys.argv[1]
zip_dest = sys.argv[2]

shutil.make_archive(zip_dest, 'zip', zip_source)
