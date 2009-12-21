#!/usr/bin/env python
#-----------------------------------------------------------------------------
# imap.py:      utilities for reading mail via imap
#               (using std library imaplib.py)
#
# See __doc__ string below.
#
# Requires:
#   - Python 1.5.2 or >, with imaplib (standard module)
#   - module message.
#   - OS: portable
#
# TODO
#   - could be more object oriented, with classes MailBox, Folder. Message
#     and Part (borrowed from message.py) should be specialized here since 
#     some info like FLAGS could become attributes in those messages.
#
# $Id: //depot/rgutils/rgutils/imap.py#2 $
#-----------------------------------------------------------------------------
'''
Utilities for reading IMAP mail.

B{Classes}:
  - L{MailBoxSession}  -- a connection with a IMAP mailbox.
'''
__version__ = '1.2.' + '$Revision: #2 $'[12:-2]
__author__ = 'Richard Gruet', 'rjgruet@yahoo.com'
__date__    = '$Date: 2003/05/25 $'[7:-2], '$Author: rgruet $'[9:-2]
__since__ = '2000/01/18'
__doc__ += '\n@author: %s (U{%s})\n@version: %s' % (__author__[0],
                                            __author__[1], __version__)


import string, re
import imaplib

from message import trace, Message, Part

true, false = -1, 0

#-----------------------------------------------------------------------------
class MailBoxSession:
#-----------------------------------------------------------------------------
    ''' A connection with an IMAP mailbox.

        B{** Access is very limited compared to the full IMAP spec!! **}
        
        Typical usage for a mail scan::

            mb = MailBoxSession(host, user, passwd, folder)
            mb.scan()   # read messages -> mb.msgCnt
            for msgNo in range(1, mb.msgCnt+1):
                msg = mb.getMsg(msgNo, removeIt=true)
                ## process message as desired (see class: Message)...
            mb.quit()   # commit changes
    '''
    MAX_CONNECTION_ATTEMPTS = 3

    #   Defaults:
    #   --------
    MAIL_SERVER = 'melina.ina.fr'
    USER =  'rgruet'
    PASSWD = ''
    FOLDER = 'INBOX'        # initial folder

    def __init__(self, mailServer=MAIL_SERVER, user=USER, passwd=PASSWD,
                       folder = FOLDER):
        self.server = mailServer
        self.user = user
        self.passwd = passwd
        self.folder = folder        # name of current mail box (IMAP)
        trace('(connecting to %s)...' % mailServer, 20)
        
        # (Socket) connection may fail sometimes, so we try several times:
        import socket
        attempts = 0
        for i in range(MailBoxSession.MAX_CONNECTION_ATTEMPTS):
            try:
                self.imap = imaplib.IMAP4(self.server)
            except socket.error, e:
                trace('Socket error during IMAP connection: %s' % e)
                attempts = attempts + 1
                if attempts < MailBoxSession.MAX_CONNECTION_ATTEMPTS:
                    trace('-> Retry connection...')
                else:
                    trace('-> Connection failed after %d attempts' % 
                            MailBoxSession.MAX_CONNECTION_ATTEMPTS)
                    raise Exception("Can't create MailBoxSession: "
                                    "socket connection failed.")
            else:
                break
        trace('connected.', 20)

        # Log in & open mail box:
        self._exec('login', (user, passwd))
        self.selectFolder(folder)
        self.msgCnt = 0     # pending mails count
        self.msgSize = 0    # pending mails total size
        self.pendingMails = [] # list of pending mails numbers.
        
        self.scan(refresh=false)    # initial scan (refresh already done)

    def __del__(self):
        try:
            self.quit()     # Commit changes, close mail box & connection
        except:
            pass

    def __repr__(self):
        self.scan() # ??
        return '<IMAP folder "%s", user %s on %s, %d mail(s), state=%s>' % (
                self.folder, self.user, self.server, self.msgCnt, self.state())

    def scan(self, filter='(UNSEEN UNDELETED)', refresh=true):
        ''' Scans mail box for messages.
        
            Updates current pending mail list.
            
            @param filter: Selection criteria (see IMAP spec). Default is
                          to select messages not read and not marked as
                          deleted.
            @param refresh: Ensure folder is up to date.
            @return: (message count, message size) 
                     [also stored in self.msgCnt, self.msgSize]
        '''
        self.pendingMails = self.searchMails(filter, refresh)
        totalSize = 0
        for msgNo in self.pendingMails:
            totalSize = totalSize + self.getMsgSize(msgNo)
        self.msgCnt = len(self.pendingMails)
        self.msgSize = totalSize
        return (self.msgCnt, self.msgSize)

    def getMsg(self, msgNo, removeIt=false, seen=true):
        ''' Reads and returns the C{msgNo}th pending mail in current folder.

            This implicitely marks the mail as 'SEEN', so it won't appear
            in next scans. Re-scan is NOT done explicitely, you have to
            call it.
            
            NB: unlike POP3, messages nos can't be guessed from the
            pending message range [1-msgCnt[
            
            "Remove" mail from server if <removeIt> true [see L{removeMsg()}]
            Mark mail as read if <seen> true (a Seen mail doesn't
            appear in pendingMails list).
        '''
        if msgNo not in self.pendingMails:
            raise ValueError('No pending mail #%d' % msgNo)

        data = self._exec('fetch', (msgNo, '(RFC822)'))
        msgSize = int(imaplib.Literal.findall(data[0][0])[0][1])
        msgLines = string.replace(data[0][1], '\r\n', '\n') # remove CR
        msg = Message(msgSize, msgLines)
        
        if not seen:
            self.markNotSeen(msgNo)

        if removeIt:
            self.removeMsg(msgNo)
        
        return msg

    getMail = getMsg # an alias
    
    def removeMsg(self, msgNo):
        ''' Removes the given message from current folder.

            NB: This only sets the flag \Deleted. the msg appears (to scan)
            as deleted, but deletion is effective only on close [quit()]
            and can be canceled by calling undelete().
        '''
        self._exec('store', (msgNo, '+FLAGS.SILENT', r'(\Deleted)'))
        self.scan()

    removeMail = removeMsg # alias
    
    def quit(self):
        '''Commits changes, unlock/close mail box & connection.

           *Must* be called to commit changes! After this call, the object
           is no more functional!
        '''
        self._exec('close')     # close mail box, commit changes.
        self._exec('logout')    # shutdown connection to the server
        trace('(session closed with %s, changes committed)...' % self.server)

    # IMAP specific:
    # -------------
    def getMsgSize(self,  msgNo):
        ''' Returns size of message in RFC822 format.
            [IMAP specific]
        '''
        data = self._exec('fetch', (msgNo, '(RFC822.SIZE)'))
        size = re.findall('\(RFC822.SIZE (\d+)\)', data[0])[0]
        return int(size)

    
    def getFlags(self, msgNo):
        ''' Returns flags (tags) for a mail as a sequence of strings
            ('\Deleted', '\Seen', '\Recent', '\Flagged', '\Answered'...).
            [IMAP specific]
        '''
        data = self._exec('fetch', (msgNo, '(FLAGS)'))
        flags = re.findall(r'\(FLAGS \((.*?)\)', data[0])[0]
        return string.split(flags)
                
        
    def setFlags(self, msgNo, flags, rescan=false):
        ''' Sets the flags for a mail [IMAP specific].
            
            Each flag ('\Deleted', '\Seen', '\Answered', etc..) will
            be set if prefixed by a '+', cleared if prefixed by a '-'.
            @param flags: A string of flag specs separated with ' '.
                         e.g. '+\Flagged -\Seen'
            @param rescan: If TRUE and flags have changed, perform a scan()
            @return: the current set of flags for the mail.
        '''
        curFlags = self.getFlags(msgNo)

        flagsToSet = []
        for f in re.findall(r'\+(\\\w+)', flags):
            if f not in curFlags:
                flagsToSet.append(f)
        #print 'flagsToSet=', flagsToSet ##
        self._exec('store', (msgNo, '+FLAGS.SILENT', '(%s)' %
                                                string.join(flagsToSet)))
        
        flagsToClear = []
        for f in re.findall(r'-(\\\w+)', flags):
            if f in curFlags:
                flagsToClear.append(f)
        #print 'flagsToClear=', flagsToClear ##
        self._exec('store', (msgNo, '-FLAGS.SILENT', '(%s)' %
                                                string.join(flagsToClear)))
        
        if (flagsToSet or flagsToClear) and rescan:
            self.scan()
            
        return self.getFlags(msgNo)
    
    # Some shortcuts for setFlags():
    def markSeen(self, msgNo, rescan=false):
        return self.setFlags(msgNo, r'+\Seen', rescan)
    
    def markNotSeen(self, msgNo, rescan=false):
        return self.setFlags(msgNo, r'-\Seen', rescan)
    
    def markDeleted(self, msgNo, rescan=false):
        return self.setFlags(msgNo, r'+\Deleted', rescan)
    
    def markNotDeleted(self, msgNo, rescan=false):
        return self.setFlags(msgNo, r'-\Deleted', rescan)
    undelete = markNotDeleted # an alias
    
    
    def listFolders(self, pattern='*', parentFolder = '/'):
        ''' Returns the folder names matching the given pattern.

            Pattern may be a path of folders (A, A/B/C) containing
            wildcards * and %. '*' used at right end indicates to
            include all subfolders.
            [IMAP specific; folders are called 'mailboxes' in IMAP]
        '''
        if pattern[0] == '/':       # strip initial '/'
            pattern = pattern[1:]
        names = []
        for e in self._exec('list', (parentFolder, pattern)):
            if e is None:
                break
            names.append(re.findall(r'" "?(.*?)"?$', e)[0])
        return names
    
    def selectFolder(self, folderName='INBOX', filter = '(UNSEEN UNDELETED)',
                     commit=true):
        ''' Sets the given folder as current (selected).
            
            C{folderName} is case sensitive, except for 'INBOX'!!
            Changes in previous folder are committed if
            C{commit} true.
            @return: number of pending mails in new folder.
            [IMAP specific; folders are called 'mailboxes' in IMAP]
        '''
        if folderName[0] == '/':        # strip initial '/'
            folderName = folderName[1:]
        if commit and (self.state() == 'SELECTED'):
            self._exec('close')     # close current mail box
        self._exec('select', (folderName,))
        self.folder = folderName
        self.scan(filter=filter, refresh=false)     # (refresh just done)
        return self.msgCnt
    
    select = selectFolder   # an alias
        
    def searchMails(self, filter='(UNSEEN UNDELETED)', refresh=true):
        ''' Searches mails in current folder.
            @param filter: Selection criteria (see IMAP spec). Default is
                          to select messages not read and not marked as deleted.
            @param refresh: Ensure current folder's view is up to date.
            @return: The list of msg numbers (as integers)
            [IMAP specific]
        '''
        if refresh:
            self._exec('select', (self.folder,))
        data = self._exec('search', (None, filter)) # -> seq of mail #
        return map(lambda x: int(x), string.split(data[0]))
    
    def state(self):
        ''' Returns the current IMAP state as a string [IMAP specific]
            (e.g. 'SELECTED').
            
        '''
        return self.imap.state
        
    # Private:
    def _exec(self, cmd, args=()):
        ''' Executes an IMAP command.
            Raise an exception if NOK.
            Return: data if OK.
        '''
        cmd = 'self.imap.%s%s' % (cmd, repr(args))
        typ, data = eval(cmd) 
        if typ not in ('OK', 'BYE'):
            raise Exception('IMAP command "%s" failed: %s, %s' %
                                                    (cmd, typ, data))
        return data


#-----------------------------------------------------------------------------
#                           U T I L I T I E S
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
#                               T E S T S
#-----------------------------------------------------------------------------
def testMailBox(smtpServer):
    
    print 'Testing imap...'
    mb = MailBoxSession()
    print mb
    
    print 'Folders defined for %s:\n' % MailBoxSession.USER
    for name in mb.listFolders():
        print ('* Folder "%s":' % name),
        mb.selectFolder(name)
        print '%d mail(s) pending, total size: %d' % (mb.msgCnt, mb.msgSize)
    print
    
    # Send one test message to inbox folder 
    
    msgCnt0 = mb.selectFolder('INBOX')
    import smtplib
    smtp = smtplib.SMTP(smtpServer)
    From = To = 'yourName@yourServer.fr'
    subject = 'Test IMAP Python'
    msgTxt = ('From: %s\nTo: %s\nSubject: %s\n\nPython is good for you!\n'
               % (From, To, subject))
    r = smtp.sendmail(From, To, msgTxt)
    if r:
        trace("Can't send mail '%s' to %s: %s" % (subject, To, r))
    print 'Test mail "%s" sent to %s.' % (subject, To)
    
    print 'waiting for mail reception...',
    import time
    n = 0
    while n < 15:
        msgCnt, msgSz = mb.scan()
        if msgCnt > msgCnt0:
            break
        time.sleep(1)
        n = n + 1
    else:
        raise Exception('Test mail not received (time out)')
    msgNo = mb.pendingMails[-1]
    print 'OK (msg #%d)' % msgNo
    
    # Read message:
    msg = mb.getMsg(msgNo, seen=false)
    msg = mb.getMsg(msgNo)
    print msg
    if msg.From[1] != From or msg.To[1] != To or msg.Subject != subject:
        raise Exception('Mail received is corrupted (from, to or subject)')
    #print 'From=%s' % str(msg.From)
    #print 'To=%s' % str(msg.To)

    print 'Removing test message...',
    mb.removeMsg(msgNo)
    print 'OK.'
    
    # Commit changes & quit:
    mb.quit()
    print '=> Tests passed.'
    return mb

#-----------------------------------------------------------------------------
#                               M A I N
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    
    smtpServer = MailBoxSession.MAIL_SERVER
    mb = testMailBox(smtpServer)
