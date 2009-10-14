# An example using NumPtr and Numeric to interface with SWIG'ed code:

import Numeric
import NumPtr

# import swig'ed module:
import average

# Create a numeric array that we want to compute the average of:
A = Numeric.array( range(1, 100), Numeric.Float64 )

# Get a pointer to this array:
aptr = NumPtr.getpointer( A )

# Pass this pointer to your swig'ed function 'ave'
print "The average of array A is:",average.ave( len(A), aptr )
