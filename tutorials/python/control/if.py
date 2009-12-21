# basic "If"
if boolean:
    x = 1
else:
    x = 0

# Not so basic "If"
# Notice the new keywords!
if (boolean and otherboolean) or ( not boolean ):  #oops, this is just if(boolean), oh well...  :~)
    x = 1
elif not otherboolean:
    x = 0
else:
    x = 100000000000000000000 # Big numbers make if statements less boring!


