import Numeric
A = Numeric.zero( (5,5) )
A[1:3] = 1

# B is a 1D version of A
B = Numeric.ravel( A )

# Ravel is a special case for "unraveling" higher dimensional arrays into 1D arrays.
# The general function is resize:
C = Numeric.resize( A, [5*5] )

# D is the shape of A, and is 7 wherever A is (false/zero),
# and 3 wherever A is (true/non-zero)
D = Numeric.where( A, 3, 7 )

# Creates a 1D array from 0 to 100 in steps of 1 and creates it all using type 'f'
E = Numeric.arrayrange(0,100,1,'f')

# F is E, where all values of E less then 30 have been replaced by 30,
# everything greater then 60 has been replaced by 60.
F = Numeric.clip( E, 30, 60 )
