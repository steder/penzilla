"""
Context managers provide a much nicer way to
handle book keeping around your file objects.

For example context managers will automatically
close the file when the block ends.
"""

with open(filename, "w") as f:
    for name in namelist:
        f.write("%s\n"%(name,))



