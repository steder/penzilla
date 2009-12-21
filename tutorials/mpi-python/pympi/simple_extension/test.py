import mpi

# My trivial mpi module
import mpimodule

if __name__=="__main__":
    print "PYMPI: I'm processor",mpi.rank
    r = mpimodule.rank()
    if (r >= 0):
        print "mpimodule:  I'm processor",r
    else:
        print "Extension was unable to call MPI!"
