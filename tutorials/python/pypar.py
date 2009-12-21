import pypar                         # The Python-MPI interface 

numproc = pypar.size()               # Number of processes as specified by mpirunmyid =    pypar.rank()               
                                     # Id of of this process (myid in [0, numproc-1]) 
node =    pypar.get_processor_name() # Host name on which current process is running

print "I am proc %d of %d on node %s" %(myid, numproc, node)

if myid == 0: 
    # Actions for process 0 
    
    msg = "P0"  
    pypar.send(msg, destination=1)                   # Send message to proces 1 (right hand neighbour)
    msg = pypar.receive(source=numproc-1)            # Receive message from last process
                
    print 'Processor 0 received message "%s" from processor %d' %(msg, numproc-1)

else:         
    # Actions for all other processes

    source = myid-1                                  
    destination = (myid+1)%numproc                   
                          
    msg = pypar.receive(source)                      
    msg = msg + 'P' + str(myid)                      # Update message     
    pypar.send(msg, destination)                     

pypar.finalize() 
