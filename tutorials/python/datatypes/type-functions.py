#############
# Arithmetic
#############
4 + 4 == 8 
3 - 5 == -2
16 / 2 == 8
16 * 4 == 64
3 % 2 == 1 # Modulus

# Long Int Conversion - Useful for function type mismatches - Not needed here.
100000000000000000000L + long(100) == 100000000000000000100L

##########
# Strings
##########
a = "Hello"
b = "World!"

# Concatenation
a + " " + b == "Hello World!"
# Repetition and Concatenation
a * 3 + " " + b == "HelloHelloHello World!"
(a + " ") * 3 + b == "Hello Hello Hello World!"
# Indexing
b[2] == "r"
# Conversion of data to string - Sesame Street:
c = 7 # Backquote ` ` or str() operations
( a + " number " + `c` ) and ( a + " number " + str(c) ) == "Hello number 7"

########
# Lists
########
x = [1, 2, 3, 4, 5]
y = [1, 2.0, (3,4), [5], {"Hello":"World!"}]

# Append 
x.append(y) == [ 1, 2, 3, 4, 5, [1, 2.0, (3,4), [5], {"Hello":"World!"}] ]
# Concatenate - Notice the similarity to Strings
[1,2,3] + [4,5] == [1,2,3,4,5]
# Multiply/Repeat - Again, strings are similar
[1,2] * 3 == [1,2,1,2,1,2]

# Delete
del y[2]
y2 == [1, 2.0, [5], {"Hello":"World!"}]
# Or
y[2] = None
y == [1, 2.0, {"Hello":"World!"}]

# Pop - Remove and delete the last element of a list
x.pop() == 5
x == [1,2,3,4]
# Length of a list
len(x) == 4

##########
# Slicing 
##########
z = range(100) # [0, 99]
z.reverse()
z[10:19] == [89, 88, 87, 86, 85, 84, 83, 82, 81]
z.reverse()
z[:10] == [0,1,2,3,4,5,6,7,8,9]
z[5:10] == [5,6,7,8,9]


###############
# Dictionaries
###############
alpha = { "Red Fish":"Blue Fish", "One Fish":"Two Fish"}
beta = { "Bob":"(555)555-5575", "Carol":"(555)555-7757" }

# Keys
alpha.keys() == ["Red Fish", "One Fish"]
beta.keys() == ["Bob", "Carol"]
# Values
alpha.values() == ["Blue Fish", "Two Fish"]
# Indexing
alpha["Red Fish"] == "Blue Fish"
beta["Carol"] == "(555)555-7757"
# Adding to a Dictionary
beta["Dave"] = "100"
beta == { "Bob":"(555)555-5575", "Carol":"(555)555-7757", "Dave":"100" }
# Deleting an entry
beta["Dave"] = None
# Or
del beta["Dave"]
beta == { "Bob":"(555)555-5575", "Carol":"(555)555-7757" }
# Length (Size) Of a dictionary
len(alpha) == 2
# Checking for membership in a dictionary
beta.has_key("Carol") == 1
