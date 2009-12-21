# Simple Application/Script to Compress files of a
# specific type in a Directory.
# I'm using this to build the packages of
# example codes for download that are
# on the first page of this tutorial.
# Yes:  You could use Zip, Winzip, Tar, or whatever
# to pick out just the code files and so on, but this
# is just a little more fun.  
"""
Path can be a file or directory
Archname is the name of the to be created archive
"""
from zipfile import ZipFile,ZIP_DEFLATED
import os
import sys 
def zipty(path, archive, type):
    paths = os.listdir(path)
    for p in paths:
        p = os.path.join(path, p) 
        if os.path.isdir(p): 
            zipty(p, archive,type)
        elif os.path.splitext(p)[1] == type: #Just a little change here
            archive.write(p) 
    return

def ziptype(path, archname, type):
    # Create a ZipFile Object primed to write
    archive = ZipFile(archname, "w",ZIP_DEFLATED) # "a" to append, "r" to read
    # Recurse or not, depending on what path is
    if os.path.isdir(path):
        zipty(path, archive, type)
    elif os.path.splitext(path)[1] == type: #This is all we're changing
        archive.write(path)
    else:
        "Compression of \""+path+"\" was failed!" # And a failure message
    archive.close()
    return "Compression of \""+path+"\" was successful!"

instructions = "ziptype.py:  Simple zipfile creation script." + \
               "recursively zips files in a directory that match" +\
               "a specific type."+\
               "e.g.:  python zipit.py myfiles .py myfiles.zip"

# Notice the __name__=="__main__"
# this is used to control what Python does when it is called from the
# command line.  I'm sure you've seen this in some of my other examples.
if __name__=="__main__":
    if len(sys.argv) == 4:
        # ziptype("directory/path", "filetype", "archivename")
        result = ziptype(sys.argv[1], sys.argv[3], sys.argv[2])
        print result
    else:
        print instructions
        
        


