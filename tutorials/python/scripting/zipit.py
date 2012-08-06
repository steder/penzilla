# Simple Application/Script to Compress a File or Directory
# Essentially you could use this instead of Winzip
# "I hate GUI Applications like WINZIP!!!"
# "Argh!"
# "I like Python though."

"""
Path can be a file or directory
Archname is the name of the to be created archive
"""
from zipfile import ZipFile, ZIP_DEFLATED
import os  # File stuff
import sys # Command line parsing
def zippy(path, archive):
    paths = os.listdir(path)
    for p in paths:
        p = os.path.join(path, p) # Make the path relative
        if os.path.isdir(p): # Recursive case
            zippy(p, archive)
        else:
            archive.write(p) # Write the file to the zipfile
    return

def zipit(path, archname):
    # Create a ZipFile Object primed to write
    archive = ZipFile(archname, "w", ZIP_DEFLATED) # "a" to append, "r" to read
    # Recurse or not, depending on what path is
    if os.path.isdir(path):
        zippy(path, archive)
    else:
        archive.write(path)
    archive.close()
    return "Compression of \""+path+"\" was successful!"

instructions = "zipit.py:  Simple zipfile creation script." + \
               "recursively zips files in a directory into" + \
               "a single archive." +\
               "e.g.:  python zipit.py myfiles myfiles.zip"

# Notice the __name__=="__main__"
# this is used to control what Python does when it is called from the
# command line.  I'm sure you've seen this in some of my other examples.
if __name__=="__main__":
    if len(sys.argv) >= 3:
        result = zipit(sys.argv[1], sys.argv[2])
        print result
    else:
        print instructions
        
        


