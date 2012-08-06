# Simple script to Unzip archives created by
# our Zip Scripts.

import sys
import os
from zipfile import ZipFile, ZIP_DEFLATED

def unzip( path ):
    # Create a ZipFile Object Instance
    archive = ZipFile(path, "r", ZIP_DEFLATED)
    names = archive.namelist()
    for name in names:
        if not os.path.exists(os.path.dirname(name)):
            # Create that directory
            os.mkdir(os.path.dirname(name))
        # Write files to disk
        temp = open(name, "wb") # create the file
        data = archive.read(name) #read the binary data
        temp.write(data)
        temp.close()
    archive.close()
    return "\""+path+"\" was unzipped successfully."
    
instructions = "This script unzips plain jane zipfiles:"+\
               "e.g.:  python unzipit.py myfiles.zip"

if __name__=="__main__":
    if len(sys.argv) == 2:
        msg = unzip(sys.argv[1])
        print msg
    else:
        print instructions
