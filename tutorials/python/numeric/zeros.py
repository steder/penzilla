from Numeric import zeros
rows = 10
columns = 10

# Note dimensions is a tuple
dimensions = (rows,columns)
# A is an array with length(dimensions) dimensions, so it is a 2d array.
# A 3d array would have, (row, column, depth) as a dimensions tuple.
A = zeros( dimensions )

# You could also write:
A = zeros( (5,3) )

# And if you aren't a fan of 0's
B = ones( dimensions )
