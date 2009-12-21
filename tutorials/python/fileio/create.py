# Let's create a file and write it to disk.
filename = "test.dat"
# Let's create some data:
done = 0
namelist = []
while not done:
    name = raw_input("Enter a name:")
    if type(name) == type(""):
        namelist.append(name)
    else:
        break
    
    # Create a file object:
    # in "write" mode
    FILE = open(filename,"w")
    FILE.writelines(namelist)
    
    # Alternatively
    # for name in namelist:
    #       FILE.write(name)
    
    FILE.close() # this is icing, you can just exit and this will be
    # handled automagically.
