# Modules.py
# Let's import some modules:
from book import * # Notice we omit the suffix ".py" from "book.py"

import map # this has the map function and a few other neat things.
print map

# Now I can Create  Book Object:
abook = Book("Robert A. Heinlein", "Stranger In a Strange Land", ["Mars","Martians"])
print abook

# What if I didn't remember that definition for the Book object?
import book
#List's everything in the "book.py" module
dir(book) 
# Enter the help system and read about the book object. This will remind you of
# all the definitions and everything.  Very convenient when you're working at
# the command prompt.

#help(book) # Uncomment to got help on the Book Object

# Let's call some functions in map to quickly increment this list :~)
# <sarcasm>( Real exciting ! )</sarcasm>
l = range(12, 76)
for i in range(0,64):
    l = map.map( map.increment, l )
print l
