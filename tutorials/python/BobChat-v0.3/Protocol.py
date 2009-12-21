"""
Protocol.py
---
Defines the BobChat Protocol:
Message Objects,
Protocol Constants,
Commands.
"""

"""
Protocol Constants
"""

"""
Command List
"""
COMMANDS = {"KICK":"Kick a user out of the Chatroom.",
            # <KICK>username</KICK>
            "QUIT":"Kill the server, disconnect everyone, and shutdown.",
            # <QUIT>
            "EXIT":"Inform all you're quitting the chat, then quit.",
            # <EXIT>
            "PRIVATE":"Send a private message to the specified user.",
            # <PRIVATE>username</PRIVATE> 
            "_WRITE_":"Internal Command, setup Write Socket",
            # <_WRITE_>
            "_READ_":"Internal Command, setup Read Socket",
            # <_READ_>
            "JOIN":"Politely Join the Chat",
            # <JOIN>username</JOIN>
            "NICK":"Change your Nickname/Username",
            # <NICK>newname</NICK
            "EMOTE":"This one is for Rob Jacob"}
            # <EMOTE>emote type message</EMOTE>
COMMANDLIST = COMMANDS.keys()
MESSAGETYPES=['Message','Command','ServerCommand']

def splitCommand(command):
    """
    Called by the Server if self.type == 1 or 2
    Returns a tuple of the Name of the Command,
    and the argument that command requires, if anything.
    Kick takes a username,
    Exit takes a message,
    Private takes a username, etc.
    """
    cmd = command.split("<")
    # cmd = ["ANY>ANYTHING","/ANY>"]
    cmd = cmd[1].split(">") # cmd[0]=="ANY>ANYTHING"
    # cmd = ["ANY","ANYTHING"]
    if len(cmd) > 1:
        return (cmd[0],cmd[1]) # ( Command Type, Value )
    else:
            return (cmd[0],)

"""
Bob Message Objects
"""
class Message:
    """
    Message( username, message[, command, password] )

    Examples of Usage:
    1).  msg = Message('steder', 'Hey Phil, how's it going?')
      This creates a message in this format and sends it to the
      server, which timestamps it and returns it to all clients.
      It is then interpreted by the read client process into:
      'steder(4:03:21pm):  Hey Phil, how\'s it going?'
    2).  cmd = Message('steder', 'I'm out of here, bis spater!', '<EXIT>')
      This creates a message like the above command, the message is
      simply printed as a comment.  It's really just a placeholder
      for the executed command.  In this case, <EXIT> is just an example
      (I'm not settled on a command syntax yet), but intuitively
      this is the command a client sends when it wishes to disconnect
      from the chat.
      So the message object arrives at the server, and the <EXIT>
      is interpreted, which generates a message in this way:
      a).  Lookup command('<EXIT>')
      b).  'User '+username+' has left, saying:'+message
        'User steder has left, saying: I'm out of here, bis spater!'
    3).  servercommand = Message('root','Server is going down for maintenance',
    '<QUIT>','2l33t')
      OR
      bootmsg = Message('moderator', 'Die annoying guy!', '<KICK>AnnoyingGuy</KICK>', 'r0xx0r')
    """
    MESSAGETYPES=['Message','Command','ServerCommand']
    def __init__(self, username, message, command=None, password=None):
        self.username = username
        self.message = message
        self.command = command
        self.password = password
        if command != None and password != None:
            # Server Command
            self.type = 2
        elif command != None:
            # Client Command
            self.type = 1
        else:
            # Message
            self.type = 0
        # A timestamp variable.
        # All messages are touched by the server,
        # which places a timestamp on them.
        self.time = ""
        return

    def type(self):
        return MESSAGETYPES[self.type]

    def getCommand(self):
        """
        Called by the Server if self.type == 1 or 2
        Returns a tuple of the Name of the Command,
        and the argument that command requires, if anything.
        Kick takes a username,
        Exit takes a message,
        Private takes a username, etc.
        """
        cmd = self.command.split("<")
        # cmd = ["ANY>ANYTHING","/ANY>"]
        cmd = cmd[1].split(">") # cmd[0]=="ANY>ANYTHING"
        # cmd = ["ANY","ANYTHING"]
        if len(cmd) > 1:
            return (cmd[0],cmd[1]) # ( Command Type, Value )
        else:
            return (cmd[0],)

    def str(self):
        if self.type == 2:
            string = self.username+": " + self.message + \
                     "( "+ self.command + ", " + self.password + " )"
        elif self.type == 1:
            string = self.username+": " + self.message + \
                     "( "+ self.command + " )"
        elif self.type == 0:
            string = self.username+": " + self.message
        return string

    def __repr__(self):
        return self.str()

    def __str__(self):
        return self.str()

    def approve(self,time):
        self.time = time
        return
    
        
                
