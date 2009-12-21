import mpi
import random
# Create a toy dataset:

data = range( 1, 1001 ) # We know what the max will be already :-)
random.shuffle( data ) # Modifies data in place

#  Divide up the problem (if we can divide it evenly)

if( len(data) % mpi.size == 0 ):
    myrank = mpi.rank
    blocksize = len(data) / mpi.size
    start = blocksize * myrank
    end = start + blocksize
    mydata = data[ start : end ]
    print mydata
    max = -1
    for i in mydata:
        if ( i > max ):
            max = i
    maximums = mpi.gather( [ max ] )
    if ( mpi.rank == 0 ):
        max = -1
        for i in maximums:
            if ( i > max ):
                max = i
        print "The maximum value is:",max
else:
    print "Sorry, I don't know how to split up the problem, aborting!"
