"""
Context managers provide a much nicer way to
handle book keeping around your file objects:
"""

with open(filename, "w") as FILE:
    for name in namelist:
        FILE.write(name)

# As soon as execution gets here
# outside the 'with' block
# your file is closed.
