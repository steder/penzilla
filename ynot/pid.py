import atexit
import os

defaultPidFile = "ynot.pid"


def cleanupPid(fileName=defaultPidFile):
    if os.path.exists(fileName):
        os.remove(fileName)
    

def makePidFile(fileName=defaultPidFile):
    pid = os.getpid()
    f = open(fileName, "w")
    contents = "%s\n"%(pid,)
    f.write(contents)
    f.close()
    atexit.register(cleanupPid, fileName)
    
    
