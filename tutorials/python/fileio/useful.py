import os.path
# os.path - The key to File I/O
os.path.exists("bob.txt")
os.path.isfile("bob.txt") # Does bob.txt exist?  Is it a file, or a directory?
os.path.isdir("bob")
os.path.isabs("/home/me/bob.txt") # Is it an absolute path to this file?

# Creating cross platform paths
# This will be slightly different on each platform
currentdir = os.curdir
imagedir = os.path.join(currentdir, "images")

# Let's say I have a full path, and yet I want to store records based
# on the name of the file:
longpath = "/home/me/python/somefiles/junk/notjunk/blah/bingo.txt"
shortpath = os.path.basename(longpath)

# Get the type of shortpath:
print "Type of",shortpath,"is", os.path.splitext(shortpath)[1]

# os.path.walk can be used to traverse directories recursively
# to apply changes to a whole tree of files.
def callback( arg, dirname, fnames ):
    sum = 0
    for file in fnames:
        sum += os.path.getsize(file)
    arg.append(sum)

arglist = []
os.path.walk("./",callback,arglist)

sum = 0
for value in arglist:
    sum += value

print "Size of directory:",sum
