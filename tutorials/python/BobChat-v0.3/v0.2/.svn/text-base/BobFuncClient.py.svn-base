"""
BobClient.py
---
Simple Chat Client that runs the Bob Protocol.  Bob stands for ...   Um....
Nevermind.

BobClient is threaded to allow one thread to wait on user input, while another
thread processes the network connection.
BobClient's goal is to send an arbitrarily long message to the server and
recieve that message back.  In fact, messages sent by other clients to the
Server will also get echoed back onto All BobClients.  This is how we create
our little chat program.
"""

import thread, time, sys
from socket import socket, AF_INET, SOCK_STREAM
HOSTNAME = ""
PORT = 7777


# These are server side calls
#sockobj.bind((HOSTNAME, PORT))
#sockobj.listen(5)

message = ["Ping!"]
def pingBob():
    sockobj = socket(AF_INET, SOCK_STREAM)
    sockobj.connect((HOSTNAME, PORT))
    for line in message:
        sockobj.send(line)
        data = sockobj.recv(1024)
        print 'Client received:', `data`
    sockobj.close()
    return

def autoBob(message):
    sockobj = socket(AF_INET, SOCK_STREAM)
    sockobj.connect((HOSTNAME, PORT))
    done = 0
    for i in range(6):
        time.sleep(1)
        sockobj.send(message)
        data = sockobj.recv(1024)
        print 'Client received:', `data`
    sockobj.close()
    return

#------------ Threaded Stuff ----------------#
DONE = 0
# I'm using PORTS 7777 and 7778
def ChatRead(PORT):
    print "Client Initializing READS"
    readsock = socket(AF_INET, SOCK_STREAM)
    readsock.connect((HOSTNAME, PORT))
    readsock.send("<READ>")
    while not DONE:
        data = readsock.recv(1024)
        print '->', `data`
    readsock.close()
    return

def ChatWrite(PORT):
    print "Client Initializing WRITES"
    writesock = socket(AF_INET, SOCK_STREAM)
    writesock.connect((HOSTNAME, PORT))
    writesock.send("<WRITE>")
    while not DONE:
        data = raw_input(">")
        if data == "<QUIT>":
            break
        writesock.send(data)
        time.sleep(0.2)
    writesock.close()
    return

def ChatBob():
    # Start two threads, one reading, one writing
    thread.start_new(ChatRead, (7777,))
    thread.start_new(ChatWrite, (7778,))
    # We need a loop here, if this
    # function exists it kills the
    # threads.
    while not DONE:
        time.sleep(0.1) 
    return

if __name__=="__main__":
    if len(sys.argv) == 2:
        autoBob(sys.argv[1])
    else:
        ChatBob()
    
