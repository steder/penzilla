#!/usr/bin/env python
#-----------------------------------------------------------------------------
# pop3.py:      utilities for reading mail via POP3
#               (using std library poplib.py)
#
# See __doc__ string below.
#
# Requires:
#   - Python >= 1.5.1
#   - module message
#   OS: portable
#
# History:
#   -2 Dec 98: created  by Richard Gruet
#   -11 Mar 99: (RG) - s '' or -s '*' means NO filter - now the default -
#   -4 Jun 99: (RG) MailBoxSession.__init__: several connection attempts in
#               case of socket error
#   -1 Jul 99: (RG) MailScanner._scanThreadProc: log exceptions in scan loop
#   -15 oct 2000: (RG) changed trace + some clean-up.
#   -19 oct 2000: (RG) Moved Message, Part and trace fcts to message.py.
# TODO
#   -Put MailScanner in its own module, since it is independent of POP3/IMAP.
#   -Could exist a MailBox base class with derived classes pop3.MailBoxSession
#    and imap.MailBoxSession
#
# $Id: //depot/rgutils/rgutils/pop3.py#1 $
#-----------------------------------------------------------------------------
'''
Utilities for reading POP3 mail.

B{Classes}
    - L{MailScanner}      -- A generic class for scanning POP3 mail boxes.
    - L{MailBoxSession}   -- A connection with a POP3 mailbox.
'''
__version__ = '1.1.' + '$Revision: #1 $'[12:-2]
__author__ = 'Richard Gruet', 'rjgruet@yahoo.com'
__date__    = '$Date: 2003/05/23 $'[7:-2], '$Author: rgruet $'[9:-2]
__since__ = '1998/12/02'
__doc__ += '\n@author: %s (U{%s})\n@version: %s' % (__author__[0],
                                            __author__[1], __version__)

from poplib import *
import time, threading, string, types

from message import Message, Part, trace, setLogVerbosity, setVerbosity, setLog

true, false = -1, 0

#-----------------------------------------------------------------------------
class MailScanner:
#-----------------------------------------------------------------------------
    ''' Periodic scan of a POP3 mailbox.
    '''
    # Class attributes:
    # ----------------
    #   Defaults:
    #   --------
    MAIL_SERVER = 'pop.free.fr'
    USER =  'rgruet'
    PASSWD = 'xxxx'
    SUBJECT = ''    # any subject
    SCAN_INTERVAL = 300 # seconds (= 5mn)

    VALID_OPTIONS = '''Valid options :

        -h <host>       POP3 server IP address [default: %s]
        -u <user>       mailbox user name [default: %s]
        -p <password>   mailbox user password [default: %s]
        -s <subject>    mail filter on subject content, or '' (or '*') [default: %s]
        -f <freq>       mailbox scan interval in sec [default: %d]
        -l <path>       log actions in file <path> [default: no log]
        -v <level>      screen verbosity level: the higher, the more detailed trace
                        on screen -1=No trace [default: 0]
        -w <level>      log verbosity level: the higher, the more detailed trace
                        on log [default: 100]
        -?              This help
        ''' % (MAIL_SERVER, USER, PASSWD, SUBJECT, SCAN_INTERVAL)

    STOP_TIMEOUT = 10   # time out between stop request and actual stop (sec, float)

    def __init__(self, options='', autoStart=true):
        '''Constructor.
           @param options: [string, or list in sys.argv style] see
                           L{VALID_OPTIONS}.
        '''
        # Parse options:
        import getopt, sys, types
        if type(options) == types.StringType:
            options = parseArgs(options)
        try:
            optList, args = getopt.getopt(options, 'h:u:p:s:f:l:v:w:?')
        except getopt.error, e:
            print '%s\n%s' % (e, self.VALID_OPTIONS)
            raise

        self.host = self.MAIL_SERVER            # set defaults
        self.user = self.USER
        self.subject = self.SUBJECT
        if not self.PASSWD:
            self.PASSWD = raw_input('passwd for user "%s" ? ' % self.USER)
        self.passwd = self.PASSWD
        self.scanInterval = self.SCAN_INTERVAL
        log = None
        verbosity = 0
        logVerbosity = 10000

        for opt, value in  optList:
            if opt == '-h': self.host = value
            elif opt == '-u': self.user = value
            elif opt == '-p': self.passwd = value
            elif opt == '-s':
                value = string.strip(value)
                if value == '*':
                    value = ''
                self.subject = value
            elif opt == '-f':
                #print 'option -f !!' ########"
                value = int(value)
                if value < 1:
                    raise ValueError('bad scan Frequency (must be >0)')
                self.scanInterval = value
            elif opt == '-l':
                log = open(value, 'w')
            elif opt == '-v':
                verbosity = int(value)
            elif opt == '-w':
                logVerbosity = int(value)
            elif opt == '-?':
                print self.VALID_OPTIONS
                return

        setLog(log)
        setVerbosity(verbosity)
        setLogVerbosity(logVerbosity)
        
        self._scanThread = None
        trace('Created %s, options="%s"' % (self,  string.join(options)))
        if autoStart:
            self.start()

    def __del__(self):
        self.stop()
        trace('MailScanner deleted ')

    def __repr__(self):
        if self._scanThread is not None: state = 'started'
        else: state = 'stopped'
        return '<%s (%s): user "%s" on host "%s", freq=%d sec>' % (
                self.__class__.__name__, state, self.user, self.host,
                self.scanInterval)

    def start(self):
        if self._scanThread is None:
            # launch scan thread
            self._stopRequest = false
            self._scanThread = threading.Thread(
                                target=MailScanner._scanThreadProc,
                                name='Pop3 mail scanner',
                                args=(self,))
            self._scanThread.start()
            trace('Mail scan started, frequency = %d sec.' % self.scanInterval)

    def stop(self):
        if self._scanThread is not None:
            if self._scanThread.isAlive():
                # request stop & wait for thread termination:
                self._stopRequest = true
                self._scanThread.join() # can't use a timeout, threading.py bugged!
                #self._scanThread.join(self.STOP_TIMEOUT)
                if self._scanThread.isAlive():
                    trace("Time out - can't stop scan thread!")
                self._scanThread = None
                trace('Mail scan stopped.')

    def handleMsg(self, msg):
        ''' Handles a Message.

            This fct is called by the scan thread for every message found.
            It must return true (non 0) if the message must be removed from
            the mailBox, false (0) otherwise.
            
            => Override this fct as necessary to implement the desired behaviour.
        '''
        return false ##TODO should be true!

    def _scanThreadProc(self):
        ''' Main procedure for the scan thread.

            Every C{scanInterval} seconds, the target mail box is scanned for mail.
            
            For each message present, the function L{handleMsg} is called as
            follow::
                handleMsg(msg)
            where msg is a Message instance (defined in this module)
            The fct must return true (non 0) if the message is to be deleted,
            false otherwise.

            The thread may be stopped by calling the method L{stop()}. The
            thread will stop ASAP.
        '''
        trace('Scan thread started.')
        try:
            while not self._stopRequest:
                try:
                    # Open session with POP3 server and check if mail present :
                    mb = MailBoxSession(self.host, self.user, self.passwd)

                    for msgNo in range(1, mb.msgCnt+1):     # process messages
                        if self._stopRequest:
                            break
                        msg = mb.getMsg(msgNo, removeIt=false)
                        trace('Message read: %s' % msg)
                        try:
                            removeIt = self.handleMsg(msg)
                        except Exception, e:
                            trace('*Exception while handling msg: %s' % e)
                        else:   # ok:
                            #trace('Message %s handled.' % msg)
                            if removeIt:
                                mb.removeMsg(msgNo)
                                trace('Message %s deleted.' % msg)
                    mb.quit()   # commit changes
                except Exception, e:
                    trace('*Exception in MailScanner._scanThreadProc loop: %s' % e)

                # Wait for next scan by sleeping, but check for stop request every second:
                for second in range(self.scanInterval):
                    if self._stopRequest:
                        break
                    time.sleep(1)
        finally:
            trace('Scan thread ended.')



#-----------------------------------------------------------------------------
class MailBoxSession:
#-----------------------------------------------------------------------------
    ''' A connection with a given POP3 mailbox.

        Access is locked and all changes uncommitted until L{quit()} is called,
        thus typical usage is only for B{one} scan::

            mb = MailBoxSession(host, user, passwd)
            mb.scan()   # read messages -> mb.msgCnt
            for msgNo in range(1, mb.msgCnt+1):
                msg = mb.getMsg(msgNo, removeIt=true)
                ## process message as desired (see class: Message)...
            mb.quit()   # commit changes
    '''
    MAX_CONNECTION_ATTEMPTS = 3

    #   Defaults:
    #   --------
    MAIL_SERVER = 'pop.free.fr'
    USER =  'rgruet'
    PASSWD = ''

    def __init__(self, mailServer=MAIL_SERVER, user=USER, passwd=PASSWD):
        self.server = mailServer
        self.user = user
        trace('(connecting to %s)...' % mailServer, 20)

        # (Socket) connection may fail sometimes, so we try several times:
        import socket
        attempts = 0
        for i in range(MailBoxSession.MAX_CONNECTION_ATTEMPTS):
            try:
                self.pop = POP3(mailServer)     # embedded POP3 object
            except socket.error, e:
                trace('Socket error during POP3 connection: %s' % e)
                attempts = attempts + 1
                if attempts < MailBoxSession.MAX_CONNECTION_ATTEMPTS:
                    trace('-> Retry connection...')
                else:
                    trace('-> Connection failed after %d attempts' % MailBoxSession.MAX_CONNECTION_ATTEMPTS)
                    raise Exception("Can't create MailBoxSession: socket connection failed.")
            else:
                break
        trace(self.pop.getwelcome(), 1000)

        # open user's mail box:
        self.pop.user(user)
        if not passwd:
            passwd = raw_input('passwd for user "%s" ? ' % user)
        self.pop.pass_(passwd)  # warning: mailbox is locked until pop.quit()
                                #is called
        self.msgCnt = 0     # unread pending messages
        self.msgSize = 0    # pending messages total size
        self.scan()         # initial scan

    def __del__(self):
        try:
            self.pop.quit()     #Commit changes, close mail box & connection
        except:
            pass

    def __repr__(self):
        self.scan() # ??
        return '<MailBoxSession for user: %s on server: %s, %d message(s)>' % (
                self.user, self.server, self.msgCnt)

    def scan(self):
        ''' Scans mail box for new messages.
            @return: (message count, message size) [also stored in
                     self.msgCnt, self.msgSize]
        '''
        self.msgCnt, self.msgSize = self.pop.stat()
        return (self.msgCnt, self.msgSize)

    def getMsg(self, msgNo=1, removeIt=false):
        ''' Reads and returns the <msgNo>th pending message.

            "Remove" it from server if C{removeIt} true [see L{removeMsg()}]
        '''
        if not (0 < msgNo <= self.msgCnt):
            raise ValueError('No such message number (%s)' % msgNo)
        r = self.pop.retr(msgNo) # -> (server response, lines list, msg length)
        msg = Message(r[2], r[1])

        if removeIt:
            self.removeMsg(msgNo)
            self.scan()
        return msg

    def removeMsg(self, msgNo=1):
        ''' Removes the C{msgNo}th pending message from the mailBox.

            NB: the msg appears (to scan) as deleted, but deletion is effective
            only on close [see L{quit()}]
        '''
        self.pop.dele(msgNo)

    def quit(self):
        '''
        Commits changes, unlock/close mail box & connection.

        B{Must} be called to commit changes! After this call, the object
        is no more functional!
        '''
        self.pop.quit()
        trace('(session closed with %s, changes committed if any)...' %
                                                                self.server)


# Argument parsing:
# ----------------
def parseArgs(argString):
    '''
    Parses a shell command argument string into a sys.argv-style list of 
    args.

    Handle the case of args enclosed into "" and including spaces (such as
    file names).

    @param argString: argument string to parse.
    @return: list of args
    '''
    import types
    if type(argString) != types.StringType:
        raise TypeError('arg must be a string')

    argList = []    # target argument list
    subArgs = []    # args enclosed by "" and including spaces
                    # must be concatenated
    for arg in string.split(argString):
        if arg[0] == '"':
            if subArgs: argList.append(string.join(subArgs))
            subArgs.append(arg[1:])
        elif arg[-1] == '"':
            subArgs.append(arg[:-1])
            argList.append(string.join(subArgs))
            subArgs = []
        else:
            if subArgs:
                subArgs.append(arg)
            else:
                argList.append(arg)
    if subArgs:                      # missing closing "
        argList.append(string.join(subArgs))
    return argList

def _strip2Quotes(s):
    ''' Strip "" around string <s> if any.
    '''
    try:
        if s[0]==s[-1]=='"':
            s = s[1:-1]
    except:
        pass
    return s


#-----------------------------------------------------------------------------
#                               T E S T S
#-----------------------------------------------------------------------------
def testScan():
    import os, tempfile
    log = os.path.join(tempfile.gettempdir(), 'mailscan.log')
    print '(log is in file %s)' % log
    s = MailScanner('-f 10 -v 0 -l "%s"' % log)
    return s

def testMailBox(user, passwd=''):
    setVerbosity(100)
    mb = MailBoxSession(user=user, passwd=passwd)
    print '%s message(s) in mailBox "%s":' % (mb.msgCnt, mb.user)
    for msgNo in range(1, min(mb.msgCnt+1, 40)):
        print '\n*** Message #%d' % msgNo
        msg = mb.getMsg(msgNo, removeIt=false)
        print msg
        print 'message has %d part(s):' % len(msg.parts)
        for part in msg.parts:
            print '\n============================================'
            print part

    mb.quit()

#-----------------------------------------------------------------------------
#                               M A I N
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    testMailBox('rgruet')
    #s = testScan()
