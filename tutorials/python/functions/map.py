# map.py
# We can use append here
def map( fun, list ):
    nlist = []
    for item in list:
        nlist.append( fun( item ) )
    return nlist
# But here we have to use concatenation, or the + operator for lists.
def rmap ( fun, list ):
    if list == []:
        return []
    else:
        return [fun( list[0] )] + rmap( fun, list[1:] )

# Make a sample test function
def increment(x):
    return x+1

# Test them out!
map( increment, [1,2,3,4,5] )
# should return [2,3,4,5,6]
map( increment, [1,2,3,4,5] ) == rmap( increment, [1,2,3,4,5] )
# There outputs should be the same!

