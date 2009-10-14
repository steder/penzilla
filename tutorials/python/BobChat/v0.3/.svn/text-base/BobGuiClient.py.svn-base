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



import thread, time, sys,string
from socket import socket, AF_INET, SOCK_STREAM

# Bob Protocol
import Protocol
# We need to pickle these messages for transmission
import pickle

# I used to Define the Text Gui Class Here, now let's just import it:
import BobClient

# Create  A GUI Client:
#   +First Define Some GUI Widgets!
from Tkinter import *
class ScrolledText(Frame):
    def __init__(self, parent=None, event=None, text='',
                 height=10, width=10):
        Frame.__init__(self, parent, event=None)
        self.event = event
        self.makewidgets(height, width)
        self.settext(text)
    def makewidgets(self, height, width):
        sbar = Scrollbar(self)
        text = Text(self, relief=SUNKEN)
        sbar.config(command=text.yview)       # xlink sbar and text
        text.config(yscrollcommand=sbar.set,   # move one moves other
                    height=height,
                    width=width)
        sbar.pack(side=RIGHT, fill=Y, expand=Y)         # pack first=clip last
        text.pack(side=LEFT, fill=BOTH, expand=Y)  #text clipped first
        self.text = text
        self.buffer = []
        # Bind Some event to this widget.
        if self.event != None:
            # If this is an imput widget, bind return
            if self.event == "input":
                self.text.bind("<Return>",self.cSetText,"")
    def settext(self, text=''):
        self.text.delete('1.0', END)
        self.text.insert('1.0', text)
        self.text.mark_set(INSERT,'1.0')
        self.text.focus()
    # For Input Handling Text Boxes
    def cSetText(self, event):
        txt = self.gettext()
        self.settext("")
        if txt.strip("\n") == "":
            """Empty String, Don't Bother"""
            return
        else:
            # Process txt to remove newlines
            # at the beginning of the string
            txt = txt.strip("\n")    
            self.buffer.append(txt)
            print self.buffer
            
    # What I'll probably use in BobChat
    def inserttext(self, text):
        self.text.insert(END, text)
    def gettext(self):
        return self.text.get('0.0',END)
    def getReference(self):
        return self

class GClient(BobClient.Client):
    # I'm using PORTS 7777 and 7778
    """
    GClient is essentially BobClient.Client.  The __init__ method of
    the two functions is exactly the same.  The real difference is
    the addition of all the gui calls in GClient.
    """
    def Chat(self):
        # Create a GUI consisting of the above widgets
        # Create main window
        win = Tk()
        win.title("BobChat: "+self.username)
        win.focus_set()
        win.protocol('WM_DELETE_WINDOW', win.quit)
        frame = Frame(win).pack()
        # Create 2 Gui Widgets:  Text Window (Scrollable)
        message_window = ScrolledText(win, "","", height=30, width=100)
        #message_window.config(width=80,height=25)
        message_window.pack(side=TOP, expand=Y, fill=BOTH)
        # Text Input (Non-Scrollable)
        input_window = ScrolledText(win,"input","", height=5, width=100)
        #input_window.config(width=80,height=5)
        input_window.pack(side=BOTTOM, expand=Y, fill=BOTH)
        input_window.config(height=10)
        # Start two threads, one reading, one writing
        print input_window

        # Comment These Out to Debug the Gui \/
        thread.start_new(self.GChatRead,
                         (self.PORTS[0],self.username,
                          message_window,))
        thread.start_new(self.GChatWrite,
                         (self.PORTS[1],self.username,
                          input_window,))
        # Comment These Out to Debug the Gui ^
        
        # We need a loop here, if this
        # function exits it kills the
        # threads.
        win.mainloop()
        win.destroy()
        return
    
    def GChatRead(self, PORT,username, msgbox):
        print "Client Initializing READS"
        # Initialize Network Connection
        readsock = socket(AF_INET, SOCK_STREAM)
        readsock.connect((self.HOSTNAME, PORT))
        self.Read(PORT,username, readsock)
        # Enter Read Loop until program exit
        while not self.DONE:
            data = readsock.recv(1024)
            if not data:
                continue
            data = pickle.loads(data)
            msg = data.str() # Get string representation of data
            # Add a newline to the beginning of the message
            # if necessary.
            temp = len(msg)
            if msg[temp-1] == "\n":
                msgbox.inserttext(msg)
            else:
                msgbox.inserttext(msg+"\n")
        readsock.close()
        return
    
    def GChatWrite(self, PORT, username, msgbox):
        # Open The Network Connection:
        print "Client Initializing WRITES"
        # Initialize Network Connection
        writesock = socket(AF_INET, SOCK_STREAM)
        writesock.connect((self.HOSTNAME, PORT))
        self.Write(PORT,username, writesock)
        join = Protocol.Message(username, "\\join")
        join.isCommand()
        writesock.send(pickle.dumps(join))
        # widget is the input widget
        # Input TO THE NETWORK!
        done = 0
        # Enter Write Loop until program exit.
        while not done:
            if len(msgbox.buffer)>0:
                #print "msgbox has ",len(msgbox.buffer),"messages!"
                # Get data from the buffer
                data = msgbox.buffer[0]
                # Send message
                message = Protocol.Message(username, data)
                message.isCommand()
                writesock.send(pickle.dumps(message))
                # print message
                # Now Delete from the buffer
                msgbox.buffer.remove(data)
            time.sleep(0.2)
        writesock.close()
        return
    
if __name__=="__main__":
    if len(sys.argv) == 2:
        Bob = GClient("",sys.argv[1])
        Bob.Chat()
    else:
        name = raw_input("Please enter a name to chat:")
        host = raw_input("Enter Host to Connect to(Enter for Default):")
        Bob = GClient(host,name)
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



    
