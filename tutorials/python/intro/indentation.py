# Example of some needlessly complicated loops and other control
# structures to illustrate how indentation is used to make
# blocks of code.
# Indentation works like { and } in C or Java.

if "hello" == "world": #Colons are used at the end of control statements a lot
    # Notice the indent here
    print "hello" + "world" + "!!!"
elif type(a) == type(1):
    newlist = []
    while a < 100: # Everything below here is part of this while
        list.append(a)
        for value in list: # Everything below here is part of this for
            try:
                newlist.append[math.sqrt(value)]
            except:
                print "crap!  value just happened to be negative!!!"
                print "I'm melting!"
        # The for loop ends here
        a += 1
    # The while loop ends here
    print newlist
# The if else structure (and in this case, the "program") ends here.

