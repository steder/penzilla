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

# Bob Protocol
import Protocol
# We need to pickle these messages for transmission
import pickle

# Build a Client Object:
class Client:
    def __init__(self, HOSTNAME,  username):
        self.HOSTNAME = HOSTNAME
        self.PORTS = [7777,7778]
        self.username = username
        self.DONE = 0
    #------------ Threaded Stuff ----------------#
    # I'm using PORTS 7777 and 7778
    def Chat(self):
        # Start two threads, one reading, one writing
        thread.start_new(self.ChatRead, (self.PORTS[0],self.username,))
        thread.start_new(self.ChatWrite, (self.PORTS[1],self.username,))
        # We need a loop here, if this
        # function exists it kills the
        # threads.
        while not self.DONE:
            time.sleep(0.1) 
        return
    
    def ChatRead(self, PORT,username):
        print "Client Initializing READS"
        # Create Connect _READ_ Message
        connect = Protocol.Message(username,"Connecting Client Read Thread",
                               "<_READ_>",None)
        # Initialize Network Connection
        readsock = socket(AF_INET, SOCK_STREAM)
        readsock.connect((self.HOSTNAME, PORT))
        # PIckle and send the connect message as a string
        readsock.send(pickle.dumps(connect))
        while not self.DONE:
            data = readsock.recv(1024)
            if not data:
                continue
            data = pickle.loads(data)
            print data.username+"( "+data.time+" ): "+data.message
        readsock.close()
        return
        
    def ChatWrite(self, PORT, username):
        print "Client Initializing WRITES"
        # Create Connect _WRITE_ Message
        connect = Protocol.Message(username,"Connecting Client Write Thread",
                                   "<_WRITE_>",None)
        # Initialize Network Connection    
        writesock = socket(AF_INET, SOCK_STREAM)
        writesock.connect((self.HOSTNAME, PORT))
        writesock.send(pickle.dumps(connect))
        while not self.DONE:
            data = raw_input(">")
            if data == "":
                continue
            else: # Just a normal message
                message = Protocol.Message(username,data)
                writesock.send(pickle.dumps(message))
                time.sleep(0.2)
        writesock.close()
        return

if __name__=="__main__":
    if len(sys.argv) == 2:
        Bob = Client("",sys.argv[1])
        Bob.Chat()
    else:
        name = raw_input("Please enter a name to chat:")
        Bob = Client("",name)
        Bob.Chat()
        

#------------ Testing Functions --------------#
# These may be useful if you rewrite them
# to use the new message objects.

## message = ["Ping!"]
## def pingBob():
##     sockobj = socket(AF_INET, SOCK_STREAM)
##     sockobj.connect((HOSTNAME, PORT))
##     for line in message:
##         sockobj.send(line)
##         data = sockobj.recv(1024)
##         print 'Client received:', `data`
##     sockobj.close()
##     return

## def autoBob(message):
##     sockobj = socket(AF_INET, SOCK_STREAM)
##     sockobj.connect((HOSTNAME, PORT))
##     done = 0
##     for i in range(6):
##         time.sleep(1)
##         sockobj.send(message)
##         data = sockobj.recv(1024)
##         print 'Client received:', `data`
##     sockobj.close()
##     return



# I'm not going to bother implementing these until
# They are supported on the server
# and the Client is Object Oriented.

##         if data.find("<QUIT>")>0 and data.find("</QUIT>")>0:
##             cmd = Protocol.splitCommand(data)
##             password = cmd[1].split(":")[1]
##             message = Protocol.Message(username,
##                                        "Server Is Exiting!", data, password)
##         elif data == "<EXIT>":
##             message = Protocol.Message(username,"left the building.","<EXIT>")
##             print "Client Exiting..."
##             time.sleep(1.0)
##             break
## # Not sure how to implement Nick at the moment
## # Let's not worry about it for now.
## ##         elif data.find("<NICK>")>0 and data.find("</NICK>")>0:
## ##             cmd = Protocol.splitCommand(data)
## ##             newname = cmd[1]
## ##             message = Protocol.Message(newname, " <=> "+username, data)
##         elif data.find("<KICK>")>0 and data.find("</KICK>")>0:
##             cmd = Protocol.splitCommand(data)
##             password = cmd[1].split(":")[1]
##             message = Protocol.Message(username, data, data, password)
##         elif data.find("<EMOTE>")>0:
##             cmd = Protocol.splitCommand(data)
##             emotion = cmd[1]
##             message = Protocol.Message(username, emotion, data)



    
