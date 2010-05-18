"""
This file handles daemonizing the ynot process

Credit goes to Chad J. Schroeder,
author of: http://code.activestate.com/recipes/278731-creating-a-daemon-the-python-way/

"""

import atexit
import fcntl
import os
import resource		# Resource usage information.
import sys


defaultPidFile = "ynot.pid"
defaultLogFile = "ynot.log"
defaultMaxFD = 1024

REDIRECT_TO = defaultLogFile


def cleanupPid(fileName=defaultPidFile):
    if os.path.exists(fileName):
        os.remove(fileName)
    

def makePidFile(fileName=defaultPidFile):
    print "make pid file"
    pid = os.getpid()
    if not os.path.exists(fileName):
        fd = os.open(fileName, os.O_RDWR|os.O_CREAT)
        fcntl.flock(fd, fcntl.LOCK_EX)
        contents = "%s\n"%(pid,)
        os.write(fd, contents)
        os.close(fd)
        atexit.register(cleanupPid, fileName)
    else:
        raise RuntimeError("%s pid file already exists, this file is either stale or there is already an instance of ynot running"%(fileName,))
    

def daemonize():
    """ Creates a child process, shuts down
    the parent process, and then redirects the io streams
    to a log file or /dev/null.

    This function assumes that it is called before
    files lot's of file descriptors or sockets are opened
    as it makes no attempt to clean up all parent file descriptors.
    
    """

    # 1. first, fork twice to drop your connections to any
    # terminals and to prevent zombie processes.
    pid = os.fork()
    if pid == 0:
        print "child"
        # setsid requires root?
        os.setsid() # establish a new process group

        # fork again: 
        pid2 = os.fork()
        if pid2 == 0:
            print "second child"
            os.umask(027) # 0750 -> -rwxr-x---
        else:
            print "first child exiting"
            os._exit(0)
    else:
        print "parent exiting"
        os._exit(0)

    # 2. ditch all current file descriptors
    print "closing file descriptors"
    maxfd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
    if (maxfd == resource.RLIM_INFINITY):
        maxfd = defaultMaxFD
    for fd in range(0, maxfd):
        try:
            os.close(fd)
        except OSError:	# ERROR, fd wasn't open to begin with (ignored)
            pass
    print "closed!"
        
    # redirect standard IO
    #print "redirecting"
    #os.open(REDIRECT_TO, os.O_RDWR)	# standard input (0)
    #os.dup2(0, 1)			# standard output (1)
    #os.dup2(0, 2)			# standard error (2)
    print "making pid file"
    makePidFile()
   

        
