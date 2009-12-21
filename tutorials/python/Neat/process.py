#!/usr/bin/env python
#-----------------------------------------------------------------------------
# process.py:           Simple process management
#
# $Id: //depot/rgutils/rgutils/process.py#1 $
#
# See __doc__ string below
#
# Requires:
#   Python 1.5.2 or >;
#   Win32 extensions on Windows
#   Threads enabled on POSIX
#   OS: Win32, Posix (Unix)
#
# TODO
#   - implement the case 'detached' on Unix.
#-----------------------------------------------------------------------------
'''
Simple process management.

Allows to launch, kill and see the status of a process independently
from the platform (at least on Win32 and Unix).

B{Classes}
  -  L{Process}         -- Abstract base class for a process.
  -  L{Win32Process}    -- a WIN32 process.
  -  L{PosixProcess}    -- a POSIX (Unix) process.

B{Usage}
    - Execute a cmd in a separate process: p = createProcess(cmd)
    - "Wrap" an existing process (pid): p = wrapProcess(pid)
'''
__version__ = '1.1.' + '$Revision: #1 $'[12:-2]
__author__ = 'Richard Gruet', 'rjgruet@yahoo.com'
__date__    = '$Date: 2003/05/23 $'[7:-2], '$Author: rgruet $'[9:-2]
__since__ = '2000/11/28'
__doc__ += '\n@author: %s (U{%s})\n@version: %s' % (__author__[0],
                                            __author__[1], __version__)

import os, sys, string, re, time

true, false = -1, 0

class ProcessError(Exception):
    ''' Exception raised by the process module.
    '''
    pass

#-----------------------------------------------------------------------------
class Process:
#-----------------------------------------------------------------------------
    ''' Abstract base class for a Process.
        => Derive specialized classes for each OS.
    '''
    MIN_LIFE_TIME = 1.0 # Minimum lifetime of a process in sec

    def __init__(self, cmd, pid, detached):
        ''' Runs the program C{cmd} in a new process or wraps the given
            process.

            NB: this base class constructor MUST be called by derived classes
            to initialize attributes.

            @param cmd:  The program command line (may be None).
            @param pid:  The process ID (in case of wrap)
            @param detached: (if creation) Whether the process will survive its
                            parent.

        '''
        self.cmd = cmd
        self.pid = pid
        self.detached = detached
        self.exitCode = None
        self.killed = false
        self.startedOn = time.time()    # N.S. if not launched by us

    def __repr__(self):
        exitCode = self.getExitCode()
        if exitCode is None:
            state = 'alive'
        else:
            state = 'ended, exit code=%d' % exitCode
        return '<%s pid=%d, %s>' % (self.__class__.__name__, self.pid, state)

    def getCmd(self):
        ''' Returns the command string executed by the process.
        '''
        return self.cmd

    def getPid(self):
        ''' Returns the PID of the process.
        '''
        return self.pid

    def wait(self, timeout=None):
        ''' Waits until process terminates or a timeout occurs.

            @param timeout: Time out in seconds (None=infinite).
            @return: the exit code, or None if timeout.
        '''
        raise NotImplementedError()

    def kill(self, hard=true):
        ''' Kills the process.

            Silent if the process is already terminated.
            The process will have an exit code = -1
            @param hard: [Unix] if true use signal SIGKILL, otherwise SIGTERM.
        '''
        raise NotImplementedError()

    def killed(self):
        ''' Returns true if process was killed (via kill).
        '''
        return self.killed

    def getExitCode(self):
        ''' Returns the exit code of the process, or C{None} if still alive.

            On Posix the process must be a child process of the caller; in some
            circumstances (kill) the exit status cannot be determined and will
            arbitrarily be returned as -1.

            The returned exit code is also assigned to self.exitCode.
        '''
        raise NotImplementedError()

    def isAlive(self):
        ''' Returns true if process is alive.
        '''
        return self.getExitCode() is None


    # Private:

    def _ensureMinLifeTime(self, minTime=None):
        ''' Sleeps until the process has lived at least C{minTime} sec.

            This is used to avoid killing the process too fast (this leads
            to strange result codes).
        '''
        if minTime is None:
            minTime = self.MIN_LIFE_TIME
        delta = time.time() - (self.startedOn + minTime)
        if delta < 0:
            time.sleep(-delta)



if sys.platform == 'win32':
    try:
        from win32process import CreateProcess, TerminateProcess, GetExitCodeProcess, STARTUPINFO
        import win32event, win32api, win32con, pywintypes
    except ImportError, e:
        raise ProcessError("Import error: %s. Have you installed the "
                    "Python win32 extensions ?" % e)
#-----------------------------------------------------------------------------
    class Win32Process(Process):
#-----------------------------------------------------------------------------
        ''' A Win32 process.
        '''

        def __init__(self, cmd=None, pid=0, detached=false):
            ''' Runs the program C{cmd} in a new process or wraps a process.

                If C{cmd} is specified (non empty), the command is executed in
                a new process. C{pid} is non significant.
                
                If C{cmd} is empty, wraps the existing process whose pid is
                given in C{pid}.

                @param cmd: The program command line (may be None).
                @param pid: The process ID (in case of wrap)
                @param detached: (if creation) Whether the process will survive
                        its parent. On Win32 processes are independent, so
                        so this simply means that parent and child must have
                        separate consoles to avoid killing the child when the
                        parent console is closed.
            '''
            if cmd:
                if detached:
                    createFlags =  win32con.CREATE_NEW_CONSOLE
                else:
                    createFlags = 0
                hp, ht, pid, tid = CreateProcess(None, cmd, None, None, 1,
                                                 createFlags,
                                                 None, None, STARTUPINFO())
            else:
                cmd = None
                assert pid
                try:
                    hp = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS,
                                              0, pid)
                except pywintypes.error, e:
                    raise ProcessError("Can't get handle from pid=%s: %s" % (pid, e))

            self.handle = hp    # [PyHANDLE] Win32 process handle
            Process.__init__(self, cmd, pid, detached)

        def wait(self, timeout=None):
            ''' See class L{Process}.
            '''
            if timeout is not None:
                timeout = int(timeout * 1000)   # in ms
            else:
                timeout = win32event.INFINITE
            win32event.WaitForSingleObject(self.handle, timeout)
            return self.getExitCode()

        def kill(self, hard=true):
            ''' See class L{Process}.
                @param hard: Always true in this Win32 version!
            '''
            if self.isAlive():
                self._ensureMinLifeTime()
                TerminateProcess(self.handle, -1)
                self.wait()     # ensure exit code known.
                self.killed = true
                self.getExitCode() # refresh attributes

        def getExitCode(self):
            ''' See class L{Process}.
            '''
            exitCode = GetExitCodeProcess(self.handle)
            if exitCode <>  259:    # (259 means alive, keep exitCode==None)
                self.exitCode = exitCode
            return self.exitCode

else: # not on Win32
    class Win32Process: pass


if  os.name == 'posix':
    import threading

#-----------------------------------------------------------------------------
    class PosixProcess(Process):
#-----------------------------------------------------------------------------
        ''' A POSIX (Unix) process.
        '''

        SCAN_INTERVAL = 1.0     # checking process death interval in sec

        def __init__(self, cmd=None, pid=0, detached=false):
            ''' Runs the program <cmd> in a new process or wraps a process.

                If C{cmd} is specified (non empty), the command is executed in
                a new process. C{pid} is non significant.
                If C{cmd} is empty, wraps the existing process whose pid is
                given in C{pid}.

                @param cmd:  The program command line (may be None).
                @param pid:  The process ID (in case of wrap)
                @param detached: (if creation) Whether the process will survive
                        its parent. On Unix, parent and child are tied,
                        children become "zombies" if parent die (but they
                        survive). They also must survive the parent logout
                        by catching the signal NOHUP.
                        TODO: IMPLEMENT THIS !!!!
                @exception ProcessError: The program cannot be launched.
            '''
            if cmd:
                l = string.split(cmd)
                progName, args = l[0], l[1:]

                pid = os.fork()
                if not pid:     # in new process
                    #TODO Use 'nohup progName args' to implement <detached> ????
                    os.execvp(progName, args)
                else:
                    childProcess = true
            else:
                cmd = None
                assert pid != 0
                childProcess = false

            Process.__init__(self, cmd, pid, detached)

            # 'wait' for the end of the child process in a separate thread:
            self.waitThread = threading.Thread(target=self._threadMain,
                                               args = (childProcess,))
            self.waitThread.start()

        def wait(self, timeout=None):
            ''' See class Process.
            '''
            self.waitThread.join(timeout)
            return self.exitCode


        def kill(self, hard=true):
            ''' See class Process.
            '''
            if self.isAlive():
                import signal
                if hard:
                    sig = 9     # SIGKILL
                else:
                    sig = signal.SIGTERM
                self._ensureMinLifeTime()
                os.kill(self.pid, sig)
                self.waitThread.join()
                self.killed = true

        def getExitCode(self):
            ''' See class Process.
            '''
            return self.exitCode

        def _threadMain(self, childProcess):
            ''' Waits thread main proc.

                If child process, waits for its end, stores the exit status and
                exits. Otherwise (not child), just wait for the end and return
                a *dummy* exit status.
            '''
            if childProcess:
                try:
                    pid, self.exitCode = os.waitpid(self.pid, 0)
                except OSError, e:
                    if e.errno == 10:   # child process probably killed
                        #print 'CHILD KILLED: %s' % e ###
                        self.exitCode = -1  # not very meaningful !!
            else:
                # Use a ps to detect death of the process. Ideally, we should
                # use os.kill(self.pid, 0) which raise OSError with errno==3
                # (No such process), but it doesn't work (at least on Linux)
                # when the real kill and this kill are performed in separate
                # threads (the process still appears alive but "defunct"):

                cmd = 'ps -p %d|grep %d' % (self.pid, self.pid)
                while true:
                    s = os.popen(cmd).read()
                    if not s :
                        self.exitCode = 0
                        break
                    if  re.search('(?i)defunct', s):
                        self.exitCode = -1  # killed
                        break
                    time.sleep(self.SCAN_INTERVAL)


else: # not on POSIX
    class PosixProcess: pass



#-----------------------------------------------------------------------------
def createProcess(cmd, detached=false):
#-----------------------------------------------------------------------------
    ''' Runs the program C{cmd} in a new process.

        @param cmd:  The program command line.
        @param detached: (if creation) Whether the process will survive its
                        parent.
        @return: a Process object.
        @exception ProcessError: The program cannot be launched.
        @see: L{wrapProcess}
    '''
    import types
    if not isinstance(cmd, types.StringType) or not cmd:
        raise ProcessError('cmd should be a non empty string')
    if sys.platform == 'win32':
        f = Win32Process
    elif os.name == 'posix':
        f = PosixProcess
    else:
        raise ProcessError('Only Win32 and Posix (Unix) are supported.')

    return f(cmd, 0, detached)

#-----------------------------------------------------------------------------
def wrapProcess(pid):
#-----------------------------------------------------------------------------
    ''' Wraps an existing process.

        @param pid: The ID of the process to wrap.
        @return: a Process object.
        @exception ProcessError:
    '''
    if sys.platform == 'win32':
        f = Win32Process
    elif os.name == 'posix':
        f = PosixProcess
    else:
        raise ProcessError('Only Win32 and Posix (Unix) are supported.')

    return f(pid=pid)

#-----------------------------------------------------------------------------
#                               T E S T S
#-----------------------------------------------------------------------------
def test():

    print 'Testing module "process"'
    if sys.platform == 'win32':
        cmd = 'notepad'
    else:
        cmd = 'xterm'

    p = createProcess(cmd)
    print p
    assert p.isAlive()
    p.kill(hard=false)
    print p
    assert not p.isAlive()

    p1 = createProcess(cmd, detached=true)
    p2 = wrapProcess(p1.getPid())
    print p2
    assert p2.isAlive()
    p2.kill(hard=true)
    print p2
    assert not p2.isAlive()
    print p1    # same as p2

    print '=> Tests passed.'
    return p

#-----------------------------------------------------------------------------
#                               M A I N
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    p = test()
