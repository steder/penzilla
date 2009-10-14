"""
BobServer.py v0.1
---
This is the first version of the simple Bob Chat Server 
"""

import sys, time
from select import select
from socket import socket, AF_INET, SOCK_STREAM

def now():
    return time.strftime("%I:%M:%S%p",time.localtime())

# Server Constants
HOSTNAME = "" # "" == localhost
PORT = 7777

# Make main sockets for accepting new client requests.
mainsocks, readsocks, writesocks = [],[],[]

# Create an reading socket.
portsock = socket(AF_INET, SOCK_STREAM)
portsock.bind((HOSTNAME, PORT))
portsock.listen(5)

# A more serious application might open several ports for listening. (like 7777 - 7780)
# These lists are used by select.  For now we just have incoming sockets
mainsocks.append(portsock)
readsocks.append(portsock)

# Message Queue
Q = []

def ServeIt():
    # Starting Select Server:
    done = 0
    while not done:
        # The one and only call to select - There is one missing optional argument
        # in the select call which can be used to set a timeout or timeout behavior.
        readables, writeables, exceptions = select(readsocks,writesocks,[])
        for sockobj in readables:
            if sockobj in mainsocks:
                # port socket: accept new client
                newsock, address = sockobj.accept()
                print 'Connect:', address, id(newsock)
                readsocks.append(newsock)
            else:
                # This is already an open connection, handle it
                try:
                    data = sockobj.recv(1024)
                    print '\tgot', data, 'on', id(sockobj)
                    if not data:
                        sockobj.close()
                        readsocks.remove(sockobj)
                        if sockobj in writesocks:
                            writesocks.remove(sockobj)
                    else:
                        # Drop message in the Q
                        Q.append(data)
                        # Make the socket writable
                        if not (sockobj in writesocks):
                            writesocks.append(sockobj)
                except:
                    pass
        # Get ready to write
        while 1:
            if (len(writeables)==0) or (len(Q) == 0):
                break
            message = Q[0]
            # Actually Write Messages
            for sockobj in writeables:
                # Name(Time): Message
                try:
                    sockobj.send( "%s(%s): %s" % (id(sockobj), now(), message))
                    print "\tsent",message,"to", id(sockobj)
                except:
                    pass
            Q.remove(message)
                

if __name__=="__main__":
    try:
        ServeIt()
    finally:
        portsock.close()
            
            
