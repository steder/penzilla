"""
Let's create a file and write it to disk.
"""

# Let's create a file containing a list of names:
names = []

# prompt for names, stop on the first blank line:
while True:
    line = raw_input("Enter a name: ")
    if line:
        names.append(line)
    else:
        break
    
# write the names to your file:
filename = "test.dat"
print "Writing names to %s..."%(filename,)
f = open(filename,"w")
for name in names:
    f.write("%s\n"%(name,))
f.close()
