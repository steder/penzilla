"""
This file handles daemonizing the ynot process

"""

import atexit
import fcntl
import os
#import resource		# Resource usage information.
import signal

# we actually want to use gevent.fork as
# it takes care of reinitializing 
import gevent


defaultPidFile = "ynot.pid"
defaultLogFile = "ynot.log"
defaultMaxFD = 1024

REDIRECT_TO = defaultLogFile


def cleanupPid(fileName=defaultPidFile):
    print "cleanupPid:", fileName
    if os.path.exists(fileName):
        os.remove(fileName)


def makePidFile(fileName=defaultPidFile):
    print "making pid file"
    pid = os.getpid()
    if not os.path.exists(fileName):
        fd = os.open(fileName, os.O_RDWR|os.O_CREAT|os.O_EXCL)
        fcntl.flock(fd, fcntl.LOCK_EX)
        contents = "%s\n"%(pid,)
        os.write(fd, contents)
        os.close(fd)
        print "Registering cleanup function for pid file:"
        atexit.register(cleanupPid, fileName)
    else:
        raise RuntimeError("%s pid file already exists, this file is either stale or there is already an instance of ynot running"%(fileName,))
    

def handleTERM():
    """Cleans up the log file and shuts down
    """
    cleanupPid()
    raise StopIteration("Caught SIGTERM!")
    

def installSignalHandlers():
    gevent.signal(signal.SIGTERM, handleTERM)


def openLog():
    print "redirecting"
    nf = open(REDIRECT_TO, "w")	# standard input (0)
    fd = nf.fileno()
    os.dup2(fd, 1)			# standard output (1)
    os.dup2(fd, 2)			# standard error (2)


def daemonize():
    """ Creates a child process, shuts down
    the parent process, and then redirects the io streams
    to a log file or /dev/null.

    This function assumes that it is called before
    files lot's of file descriptors or sockets are opened
    as it makes no attempt to clean up all parent file descriptors.
    
    """
    # 1. ditch all current file descriptors
    # print "closing file descriptors"
    # maxfd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
    # if (maxfd == resource.RLIM_INFINITY):
    #     maxfd = defaultMaxFD
    # for fd in range(0, maxfd):
    #     try:p
    #         os.close(fd)
    #     except OSError:	# ERROR, fd wasn't open to begin with (ignored)
    #         pass
    # print "closed!"

    
    # 2. fork twice to drop your connections to any
    # terminals and to prevent zombie processes.
    pid = gevent.fork()
    if pid == 0:
        print "child"
        # setsid requires root?
        os.setsid() # establish a new process group

        # fork again: 
        pid2 = gevent.fork()
        if pid2 == 0:
            print "second child"
            os.umask(027) # 0750 -> -rwxr-x---
        else:
            print "first child exiting"
            os._exit(0)
    else:
        print "parent exiting"
        os._exit(0)
        
    # redirect standard IO
    openLog()
    makePidFile()
    installSignalHandlers()

        
