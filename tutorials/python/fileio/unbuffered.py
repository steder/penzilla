"""
 0 means buffer size of 0
 or unbuffered:

 1 means line buffered

 Some other number >1 means use
 a buffer that size (4096 would mean use a buffer
 of 4096 bytes)

 Defaults to -1, which indicates the platform
 default
"""
f = open(filename, "w", 0) 

f.writelines(namelist)

"""
Now when your program exits without
calling FILE.close() your data will
still be written to disk.

Yeah...  It kind of an ugly way to do things.

"""
