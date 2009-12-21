#!/usr/bin/env python
#----------------------------------------------------------------------------
# fwdmail.py:           Forward e-mail
#
# Usage: see __doc__ string below.
#
# Requires:
#    - Python 1.5.2 or newer (www.python.org)
#    - modules pop3, imap, message, async (package rgutils)
#    - OS: portable
#
# TODO:
#
# $Id: //depot/rgutils/scripts/fwdmail.py#4 $
#---------------------------------------------------------------------------
'''Usage: [python] fwdmail.py [options]

Forward mail and optionally remove it.

Valid options:

  -M MAXMAIL  Don't forward more than MAXMSG mails [-1: forward ALL
              pending mails]. Set to 0 to forward NO mails (default).
  -N          [IMAP only] Select only new (=UNSEEN) mails; default is to
              select all mails not flagged as 'UNDELETED' .
  -r          Remove mails from original mailbox after forward
              [default: keep them]
  -m ADDRESS  Mail server IP address (incoming mails) [default: 'melina.ina.fr']
  -i          IMAP4 server [default: POP3 server]
  -u USERNAME Name of user to forward [default: rronfard]
  -p PASSWD   User password [default: rronfard's password]
  -F FOLDER[,FOLDER...]
              [IMAP only] A list of folders to forward [default: INBOX].
              A/B means subfolder B of folder A. Each folder name may include
              wildcards * and %. '*' at end means all subfolders recursively.

  -s ADDRESS  SMTP mail server to use to send mails [default: 'melina.ina.fr']
  -f E-MAIL   Where to forward [default: ronfard@us.ibm.com]
  -t TAG      Prefix the Subject with this tag in forwarded mails.

  -l LOGFILE  Log file path [default is fwdmail.log in this script's directory]
  -h          Print this message on stdout and exit.
  -V          Print fwdmail version on stdout and exit.
'''
__version__ = '1.7.' + '$Revision: #4 $'[12:-2]
__author__ = 'Richard Gruet', 'rjgruet@yahoo.com'
__date__    = '$Date: 2003/04/29 $'[7:-2], '$Author: rgruet $'[9:-2]
__since__ = '2000/10/15'

import sys, os, string, re, getopt
from rgutils.message import trace, setLogVerbosity, setVerbosity, setLog, dumpMail
import rgutils.async

true, false =-1, 0
#SubjectHdr = re.compile(r'Subject: *([^\n]*?) *\n')

def error(msg):
    sys.stderr.write('fwdmail: error: %s\n' % msg)
    sys.exit(1)

# Parse args:
# ----------
try:
    opts, modules = getopt.getopt(sys.argv[1:], 'f:F:hil:m:M:Np:rs:t:u:V', [])
except getopt.error, e:
    error('%s\n%s' % (e, __doc__))

options = {}    # a dictionary indexed by opt is more convenient
for opt, value in opts:
    options[opt] = value

if options.has_key('-h'):
    print __doc__
    sys.exit(0)

if options.has_key('-V'):
    print 'fwdmail %d.%d.%d' % __version__
    sys.exit(0)

maxMails = int(options.get('-M', '0'))
if maxMails < 0:
    maxMails = 10000000

useImap = options.has_key('-i')
if useImap:
    from rgutils import imap
    folderSpec = options.get('-F', 'INBOX')
else:
    from rgutils import pop3

removeMails = options.has_key('-r')
if options.has_key('-N'):
    filter = '(UNSEEN UNDELETED)'
else:
    filter = '(UNDELETED)'
mailServer = options.get('-m', 'melina.ina.fr')
smtpServer = options.get('-s', 'melina.ina.fr')
user = options.get('-u', 'rronfard')
passwd = options.get('-p', 'ryxqyc5e')
forwardTo = options.get('-f', 'ronfard@us.ibm.com')
tag = options.get('-t', '')
if tag: tag = tag + ' '
logPath = options.get('-l',
            os.path.join(os.path.dirname(sys.path[0]), 'fwdmail.log'))

# Do it!

print 'fwdmail %s' % __version__

print 'options = %s' % options ###

setLog(open(logPath, 'a'))
setVerbosity(100)
setLogVerbosity(100)

if useImap:
    mb = imap.MailBoxSession(mailServer, user, passwd)
    folders = []
    for folderPattern in string.split(folderSpec, ','):
        folders.extend(mb.listFolders(pattern=folderPattern))
    #print 'folders = %s' % folders ##
else:
    mb = pop3.MailBoxSession(mailServer, user, passwd)
    folders = ['']      # dummy

try:

    import smtplib
    smtp = smtplib.SMTP(smtpServer)

    try:
        for folder in folders:
            if useImap:
                mb.selectFolder(folder, filter=filter)
                mailNos = mb.pendingMails
            else:
                mailNos = range(1, mb.msgCnt+1)

            if maxMails >= 0:
                mailNos = mailNos[:maxMails]

            if mb.msgCnt > 0:
                s = '%s message(s) for user %s' % (mb.msgCnt, mb.user)
                if useImap:
                    s = s + ' in folder %s' % folder
                trace(s)

            for msgNo in mailNos:
                trace('Reading mail #%d' % msgNo)

                # Performs an asynchronous call to get message because a
                # timeout sometimes occurs:
                try:
                    from rgutils import async
                    msg = async.callWithTimeout(30, mb.getMsg, msgNo,false, 30)
                except Exception, e:
                    trace("*** Can't read mail #%d (%s) => skip it" %
                                                                (msgNo, e))
                    if removeMails:
                        mb.removeMsg(msgNo)
                        trace('Deleted mail #%d from %s on %s' % (msgNo, user,
                                                                  mailServer))
                    continue

                trace('Forwarding mail #%d "%s" to %s' % (msgNo, msg.Subject,
                                                          forwardTo))

                # Extract the message body (starting after 1st empty line:
                for i in range(len(msg.lines)):
                    line = msg.lines[i]
                    if not line:
                        break
                else:
                    dumpMail(msg)   # (see message.py)
                    raise Exception("Can't find header 'Content-Type' or "
                                    "an empty line in mail (mail dumped in "
                                    "file %s)." % dumpPath)
                body = string.join(msg.lines[i:], '\n')

                # Avoid empty 'From' header (crashes!):
                if not msg.rfc822['From']:
                    msg.From = ('? (forwarded by RGruet)', 'rgruet@ina.fr')
                    msg.rfc822['From'] = string.join(msg.From, ', ')

                if tag:
                    # Modify the 'Subject' header to add the tag:
                    try:
                        subject = msg.rfc822['Subject']
                    except KeyError:
                        subject = ''
                    msg.rfc822['Subject'] = tag + subject

                msgTxt = string.join(msg.rfc822.headers, '') + body
                r = smtp.sendmail(msg.From[1], forwardTo, msgTxt)
                if r:
                    trace("Can't send mail #%d (%s): %s" % (i, msg.Subject, r))
                elif removeMails:
                    mb.removeMsg(msgNo)
                    trace('Deleted mail #%d from %s on %s' % (msgNo,
                                                              user, mailServer))
    finally:
        smtp.quit()
finally:
    mb.quit()   # This commits the changes (mail deletions)

# Found no other way to kill the "asyncall" remaining threads (in case of timeout):
try:
    import win32api
except ImportError:
    pass
else:
    win32api.TerminateProcess(win32api.GetCurrentProcess(), 0)

