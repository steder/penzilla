import atexit
import os

defaultPidFile = "ynot.pid"


def cleanupPid(fileName=defaultPidFile):
    if os.path.exists(fileName):
        os.remove(fileName)
    

def makePidFile(fileName=defaultPidFile):
    pid = os.getpid()
    if not os.path.exists(fileName):
        f = open(fileName, "w")
        contents = "%s\n"%(pid,)
        f.write(contents)
        f.close()
        atexit.register(cleanupPid, fileName)
    else:
        raise RuntimeError("%s pid file already exists, this file is either stale or there is already an instance of ynot running"%(fileName,))
    
    
