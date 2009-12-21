"""
BobServer.py v0.4
---
Select Based Server Object,
with a threaded Admin service that allows it
to read input from the terminal on which it is started,
so that the Admin can type 'quit', or other commands
to shut the server down cleanly.

Hopefully this will cut down on the number of manual kills
(Keyboard Interrupts) that we need to do.
"""

import sys, time, thread
from select import select
from socket import socket, AF_INET, SOCK_STREAM

# Import Bob Protocol File
import Protocol
from Protocol import COMMANDS, COMMANDLIST, MESSAGETYPES
# To pickle and unpickle message objects
import pickle

class Server:
    def __init__(self, HOSTNAME, PORTS, PASSWORD):
        # Server Constants
        self.HOSTNAME = HOSTNAME
        self.PORTS = PORTS
        self.PASSWORD = PASSWORD
        # Make main sockets for accepting new client requests.
        mainsocks, readsocks = [],[]
        for PORT in PORTS:
            portsock = socket(AF_INET, SOCK_STREAM)
            portsock.bind((HOSTNAME, PORT))
            portsock.listen(5)
            mainsocks.append(portsock)
            readsocks.append(portsock)
            
        # Create Reading Sockets:
        self.mainsocks = mainsocks
        self.readsocks = readsocks
        self.writesocks = []
        
        # Message Queue
        self.Q = []
        
    def Now(self):
        return time.strftime("%I:%M:%S%p",time.localtime())
    """
    AH!!!
    Connect to myself!!!
    Create a new socket, connect, and
    send a single message, then disconnect.
    You'll get handled, and then you can issue
    commands to the server.  Just do this in another
    thread.  This way the server can be told to quit,
    instead of killing it in a messy way.
    """
    def Prompt(self,ps):
        done = 0
        print "Admin Initializing WRITES"
        # Create Connect _WRITE_ Message
        connect = Protocol.Message("__ADMIN__","Connecting Admin Write Thread",
                                   "<_WRITE_>",None)
        # Initialize Network Connection    
        writesock = socket(AF_INET, SOCK_STREAM)
        writesock.connect((self.HOSTNAME, self.PORTS[1]))
        writesock.send(pickle.dumps(connect))
        while not done:
            input = raw_input(ps)
            if input == "quit":
                message = Protocol.Message("__ADMIN__",input,
                                           "<QUIT>"+self.PASSWORD+"</QUIT>",
                                           self.PASSWORD)
                writesock.send(pickle.dumps(message))
                break
            else:
                time.sleep(0.2)
        writesock.close()
        return
    
    def Serve(self):
        # Starting Select Server:
        done = 0
        thread.start_new(self.Prompt,(">",))
        while not done:
            # The one and only call to select - There is one missing optional argument
            # in the select call which can be used to set a timeout or timeout behavior.
            readables, writeables, exceptions = select(self.readsocks,self.writesocks,[])
            for sockobj in readables:
                if sockobj in self.mainsocks:
                    # port socket: accept new client
                    newsock, address = sockobj.accept()
                    print 'Connect:', address, id(newsock)
                    self.readsocks.append(newsock)
                else:
                    # This is already an open connection, handle it
                    #try:
                    # Data is a pickled Protocol.Message object
                    data = sockobj.recv(1024)
                    if not data:
                        sockobj.close()
                        self.readsocks.remove(sockobj)
                    try:
                        data = pickle.loads(data)
                    except EOFError:
                        sockobj.close()
                        if sockobj in self.readsocks:
                            self.readsocks.remove(sockobj)
                        continue
                    print '\tgot', data, 'on', id(sockobj)
                    # Server Commands
                    print "Is it type 2:",data.type == 2
                    if data.type == 2:
                        cmd = data.getCommand()
                    #print "Is the command <QUIT>", cmd[0] == "QUIT"
                    #print "Is the password right?", cmd[1] == self.PASSWORD
                    #print "Password =", cmd[1], self.PASSWORD
                        if cmd[0] == "QUIT":
                            if cmd[1] == self.PASSWORD:
                                for sock in self.mainsocks:
                                    sock.close()
                                for sock in self.readsocks:
                                    sock.close()
                                for sock in self.writesocks:
                                    sock.close()
                                return #EXIT!
                        else:
                            print "Unhandled Command:",cmd
                    elif data.type == 1:
                        cmd = data.getCommand()
                        print "cmd = ", cmd
                        if cmd[0] == "_WRITE_":
                            """Leave in Readsocks"""
                        elif cmd[0] == "_READ_":
                            self.readsocks.remove(sockobj)
                            self.writesocks.append(sockobj)
                        else:
                            print "Unhandled Command:",cmd
                    # A Message
                    elif data.type == 0:
                        # Drop message in the Q
                        data.approve(self.Now())
                        self.Q.append(data)
                    #except:
                    #    pass
            # Get ready to write
            #print len(writeables), len(self.Q)
            while 1:
                if (len(writeables)==0) or (len(self.Q) == 0):
                    break
                message = self.Q[0]
                # Actually Write Messages
                for sockobj in writeables:
                    # Name(Time): Message
                    try:
                        sockobj.send( pickle.dumps(message) )
                        print "\tsent",message,"to", id(sockobj)
                    except:
                        pass
                self.Q.remove(message)
                
if __name__=="__main__":
    Bob = Server("",[7777,7778],"ack7778syn")
    try:
        Bob.Serve()
    finally:
        for sock in Bob.mainsocks:
            sock.close()
            
            
