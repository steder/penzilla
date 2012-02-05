# Introduction to Python's Data Structures
#
# Int and Long int(Range?)
inta = 100
def factorial (n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
    
intb = factorial(100) # 100! is pretty damned big, notice python doesn't overflow.

# Float/Double(Precision?)
floata = 1.2
floatb = 0.1 # isn't this peculiar?

# Strings(Indexing, Concatination, Searching, Matching)
s1 = "I am a string!\n"
c1 = s1[1]

# Tuples(What are they, simple examples)
t1 = (1, 2) # coordinates on a grid
t2 = ("username", "passcode") # Not a very useful "use" of a tuple

# Tuples are mostly going to be used for things like encapsulating a
# bunch of function arguments, especially things like coordinates
# that are very tightly coupled.

# Lists(What they are, append, concatenate, add, remove(del), searching, map, SLICES!)

# Now connect strings (w/slicing) to lists :~)

# Dictionaries(What they are, some neat uses, NOTES on SPEED?)
