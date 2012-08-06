# Let's define a class quick:
class Student:
    def __init__(self, name="", school="", major="", year="", gpa=-1):
        self.name = name
        self.school = school
        self.major = major
        self.year = year
        self.gpa = gpa

    def __str__(self):
        string = ["++++++++++++++++++++++", 
                 "+" + name,
                 "+" + school,
                 "+" + major,
                 "+" + year,
                 "+" + gpa,
                 "++++++++++++++++++++++"]
                 
        return "\n".join(string)

# Now I'll create a student:
Mike = Student("Mike", "UIUC", "CS", "Senior", 0.6)

# Now, let's Pickle Mike
mike_the_pickle = pickle.dumps(Mike)
print mike_the_pickle

# Now let's clone mike!
Mike2 = pickle.loads(mike_the_pickle)
if type(Mike) == type(Mike2):
    print "Mike and Mike2 are of type:", (str(type(Mike)))

# Create A Pickler
P.pickle.Pickler("pickle.dat")
# Write to your Pickler
P.dump(Mike)
# OR, combine the last 2 lines
pickle.dump(Mike, "pickle.dat")

# Now, Create an Unpickler, and get Mike back
U = pickle.Unpickler("pickle.dat")
# Read from the pickler
Mike = U.load()
# Do it in one line
Mike2 = pickle.load("pickle.dat")

# Just something to keep in mind:
# For more sophisticated usage, you may want to use the Shelve module,
# or other Database modules.
