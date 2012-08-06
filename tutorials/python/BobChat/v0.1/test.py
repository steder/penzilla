import os,sys,thread,string,time # haha, thread and string! (SORRY!)
import BobClient

letters = string.letters 

if __name__=="__main__":
    for i in range(26):
        message = letters[i]
        thread.start_new(BobClient.chatBob, (message,))
        print "Created",message,"thread!"
        time.sleep(0.2)
