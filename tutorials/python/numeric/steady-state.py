"""
file: steady-state.py

A simple 2D Steady State Heat Distribution code
(Underlying Partial Differential Equation is the Poisson Equation)

The edges of the grid are all at constant temperature, 3 sides are at 100.0 (Degrees, whatever)
1 side is at 0 degrees.

We iterate until the temperatures converge.
"""

import math
import time
import Numeric

def main( N=10, EPSILON = 0.01 ):
    # Stores Old(previous timestep) Values 
    u = Numeric.zeros( (N,N),Numeric.Float32 )
    # New(current/next timestep) Values
    w = Numeric.zeros( (N,N),Numeric.Float32 )

    # Set boundary values and compute mean boundary value
    mean = 0.0
    for i in xrange(N):
        # 3 sides @ 100.0 degrees
        u[i][0] = 100.0
        u[i][N-1] = 100.0
        u[0][i]  = 100.0
        # 1 side @ 0 degrees
    for i in xrange(N):
        u[N-1][i] = 0.0
        
    mean += Numeric.sum(u[:][0])
    mean += Numeric.sum(u[:][N-1])
    mean += Numeric.sum(u[0][:])
    mean += Numeric.sum(u[N-1][:])
    mean /= (4.0 * N)

    # Initialize interior values:
    print mean
    for i in xrange(1,N-1):
        for j in xrange(1,N-1):
            u[i][j] = mean
    print u,"\n"
    # Compute Steady-State solution:
    done = False
    iterations = 0
    while not done:
        delta = 0.0
        for i in xrange(1,N-1):
            for j in xrange(1,N-1):
                w[i][j] = u[i-1][j] + u[i+1][j] + u[i][j-1] + u[i][j+1]
                w[i][j] /= 4.0
                d = math.fabs( w[i][j] - u[i][j] ) 
                if( d > delta ):
                    delta = d
        if( delta <= EPSILON ):
            done = True
        # Copy new interior state to old:
        for i in xrange(1,N-1):
            for j in xrange(1,N-1):
                u[i][j] = w[i][j]
        iterations += 1

    # Print Solution:
    print u
    return iterations
                    
if __name__=="__main__":
    print "Starting Steady State Example:"
    start = time.time()
    iterations = main()
    end = time.time()
    print "Finished Steady State Example in",end - start,"and",iterations,"iterations."
