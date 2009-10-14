# Behold the power of a Hello World program with 
# console I/O.

print "Hello User, you're lookin' fine!"
print "Can I get your phone number?"
phonenumber = raw_input(">")

# At this point number could be a number of strings,
# from "", to "no", to "(555)555-5555"

number = raw_input("Pick a number between 1-7: ")
number = int(number) # We really should check that this is between 1-7

for i in range(number):
    print "You said your phone number was:",phonenumber
