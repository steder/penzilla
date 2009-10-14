"""
BobClient.py
---
Simple Ping Client
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

def chatBob():
    return

if __name__=="__main__":
    if len(sys.argv) == 2:
        autoBob(sys.argv[1])
    else:
        chatBob()
    
