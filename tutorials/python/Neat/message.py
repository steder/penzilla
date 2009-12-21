#!/usr/bin/env python
#-----------------------------------------------------------------------------
# message.py:               Message & Part classes
#
# See __doc__ string below.
#
#   This module defines the following classes:
#
# Requires:
#   Python >=1.5.1
#   OS: portable
#
# $Id: //depot/rgutils/rgutils/message.py#1 $
#-----------------------------------------------------------------------------
'''
This module defines 2 classes used by the modules C{pop3.py} and C{imap.py}:
    - L{Message}  -- a class representing a mail in RFC822 format.
    - L{Part} -- a class representing ONE part (or attachment) in a (possibly
      multipart) message.

It also includes some trace utilities.
'''
__version__ = '1.1.' + '$Revision: #1 $'[12:-2]
__author__ = 'Richard Gruet', 'rjgruet@yahoo.com'
__date__    = '$Date: 2003/05/23 $'[7:-2], '$Author: rgruet $'[9:-2]
__since__ = '2000/10/19'
__doc__ += '\n@author: %s (U{%s})\n@version: %s' % (__author__[0],
                                            __author__[1], __version__)

import os, sys, cStringIO, time, string, types

true, false = -1, 0

#-----------------------------------------------------------------------------
class Message:
#-----------------------------------------------------------------------------
    ''' One mail message.

        The message header is represented by object attributes (To, From,
        Subject, Date...).
        The various parts of the message body are represented as a list of
        1 to N x Part objects (see class L{Part}) in C{self.parts}.

        B{Limitations}
            - doesn't handle B{nested} multi-part messages.
            - full MIME handling is not guaranteed!
    '''
    MULTIPART = 'multipart/mixed'


    def __init__(self, msgLen, msgLines):
        ''' Constructor.
            @param msgLen: The length of the message in RFC822 format.
            @param msgLines: The message in RFC822 format, either the list
                            of message lines or the whole msg as a string.
        '''
        self.size = msgLen
        self.lines = []     # [list] message lines

        # Parse message header into attributes:
        import rfc822
        if isinstance(msgLines, types.StringType):
            self.lines = string.split(msgLines, '\n')
            lines = msgLines
        else:   # assume list
            self.lines = msgLines
            lines = string.join(msgLines, '\n')
            
        try:
            fLines = cStringIO.StringIO(lines)
            self.rfc822 = rfc822.Message(fLines, true)
            self.headers = self.rfc822.headers  # list of all header lines
                                                # (raw text)

            # Missing fields are given the value None [strings, dates] or
            # (None, None) [adresses]:
            self.Return_Path = self.rfc822.getheader('Return-Path') # a string
            self.From = self.rfc822.getaddr('From') # (name, e-mail) or (None, None)
            self.To = self.rfc822.getaddr('To')     # (name, e-mail)    "       "
            self.ID = self.rfc822.getheader('Message-ID')   # a string
            self.Subject = self.rfc822.getheader('Subject') # a string
            self.Date = self.rfc822.getdate('Date') # a 9-tuple compatible with time.mktime() or None
            self.Organization = self.rfc822.getheader('Organization') # a string
            self.MIME_Version = self.rfc822.getheader('MIME-Version') # a string

            # Resync current pos on 'Content_type' in file:
            fLines.seek(0); lastLineOffset = -1
            while true:
                line = fLines.readline()
                if not line:
                    lastLineOffset = 0
                    break
                if line[:12]  == 'Content-Type':
                    break
                lastLineOffset = fLines.tell()
            assert lastLineOffset >= 0
            fLines.seek(lastLineOffset) # back one line

            # Split the messages into its parts (one or more):
            parts = []
            part = Part(fLines, self)
            self.multipart = (part.mainType == 'multipart')

            if self.multipart:
                self.boundary = part.params['boundary']
                #trace('boundary = "%s"' % self.boundary', 10)##
                sectionDivider = '--' + self.boundary
                endMarker = self.boundary + '--'

                fLines.seek(lastLineOffset) # go one line after content-type
                fLines.readline()
                while true:
                    line = fLines.readline()
                    if line == '':
                        trace('(EOF while seeking after 1st section divider, '
                              'assume only one part (content sub-type=%s)).'
                               % part.subType)
                        fLines.seek(lastLineOffset)     # go back
                        fLines.readline()
                        break
                    elif line[:-1] == sectionDivider: # go just after boundary
                        break

                import multifile
                mf = multifile.MultiFile(fLines)
                mf.push(self.boundary)
                while true:
                    part = Part(cStringIO.StringIO(mf.read()), self)
                    parts.append(part)
                    if not mf.next():
                        break
                mf.pop()
            else:   # only 1 part:
                parts.append(part)
                
            self.parts = parts
        except:
            print '(current message dumped in %s)' % dumpMail(self)
            raise
            

    def __repr__(self):
        return '<Mail Message from: %s to: %s, subject: "%s", %d part(s)>' % (
                self.From[1], self.To[1], self.Subject, len(self.parts))


#-----------------------------------------------------------------------------
class Part:
#-----------------------------------------------------------------------------
    ''' One content (part) in a (possibly multi-part) mail message.
    '''
    def __init__(self, fMsg, hostMsg):
        ''' Constructor.

            @param fMsg: A seekable file-like input object representing the
                         target mail message part.
            @param hostMsg: The Message instance containing the part.
        '''
        import rfc822, mimetools, string, cStringIO, re

        self.msg = hostMsg                  # Message containing the part

        # Parse content-type header:
        mt = mimetools.Message(fMsg, true)
        self.type = mt.gettype()            # 'main type/subtype'
        self.mainType = mt.getmaintype()    # 'type'
        self.subType = mt.getsubtype()      # 'subtype'
        self.params = {}    # parameters for content-type {'name': 'value',...}
        for item in mt.getplist():
            # Value may include a '=', thus everything on the left of the 1st
            # '=' is considered as the key, and everything on the right is 
            # considered as the (string) value :
            l = string.split(item, '=')
            key = l[0]
            value = string.join(l[1:], '=')
            ##print 'key = "%s", value = "%s"' % (key, value) ###
            self.params[key] = _strip2Quotes(value)
        try:
            self.name = self.params['name'] # use it as file name for attachment
        except KeyError:
            self.name = None

        # Other headers:
        self.encoding = mt.getencoding()    # '7bit', 'base64'...
        fMsg.seek(0)                            # restart for rfc822
        self._rfc822 = rfc822.Message(fMsg, true)
        self.description = self._rfc822.getheader('Content-Description') # a string or None

        self.disposition = self._rfc822.getheader('Content-Disposition') # a string or none
        self.fileName = None
        if self.disposition:
            mo = re.search('filename="(.*)"', self.disposition) # parse 'filename' field
            if mo is not None:
                self.fileName = mo.group(1) # use it as file name for attachment

        # Part's body (decoded if necessary)!
        fBody = cStringIO.StringIO()
        fMsg.seek(0)            # resync after headers (=after 1st empty line)
        while fMsg.readline()[:-1] <> '':
            pass

        if self.mainType != 'multipart':
            if self.encoding in ('base64', 'quoted-printable', 'uuencode'):
                mimetools.decode(fMsg, fBody, self.encoding)
            else:
                mimetools.copyliteral(fMsg, fBody)
            self.body = fBody.getvalue()
        else:
            self.body = '<not significant>' # multi-part message

    def __repr__(self):
        return '<part: "%s", %s, encoding=%s>' % (self.getName(), self.mainType, self.encoding)

    def __str__(self):
        if len(self.body) > 500:
            body = self.body[:500] + '...'
        else:
            body = self.body
        return 'name=%s, type=%s, encoding=%s, description=%s, disposition=%s\nbody = "%s"' % (
            self.getName(), self.type, self.encoding, self.description,
            self.disposition, body)

    def getName(self):
        ''' Returns the "name" of the part.
        '''
        if self.name: return self.name
        if self.fileName: return self.fileName
        else: return '<no name>'

    def getFileName(self, computeDefault=true):
        ''' Gets the base file name to use for saving the part.

            @return: the fileName attribute of the part, or by default its
                     name. If none is defined (part == message body), either
                     compute a default name (C{computeDefault} true), or else
                     return None.
        '''
        if self.fileName:
            return self.fileName
        elif self.name:
            return self.name
        elif computeDefault:
            # Default name is 'sender_date.txt':
            date = time.strftime('%Y%m%d%H%M%S', self.msg.Date)
            return '%s_%s.txt' % (self.msg.From[1], date)
        else:
            return None

    def write(self, fileDir, fileName=None, overWriteIfExists=true):
        ''' Writes the part's body into a file.

            @param fileDir: Target file dir path (created if necessary).
            @param fileName: Target file path (created if necessary).
                if C{fileName} is not specified, use the attribute filename or 
                (if undefined) the name attribute. If the latter is undefined, 
                error!

            @param overWriteIfExists: If true, an existing file with the same
                    name will be overwritten, otherwise a suffix '_n' is
                    appended to the file name.
            @return: actual save (absolute) path.
        '''
        import os
        if not fileName:
            fileName = self.getFileName(false)
            if not fileName:
                raise Exception('No target fileName where to write')

        path = '%s\\%s' % (fileDir, fileName)

        if not overWriteIfExists:
            # If file already exists, append an indice '_n':
            n = 0
            while true:
                if n > 0:       # (not 1st time)
                    p = '%s_%d' % (path, n)
                if not os.path.exists(p):
                    break
                n = n + 1
        else:
            p = path

        # If part is unencoded text, write it in text mode (on Windows this adds
        # a CR to the LF ):
        if self.mainType == 'text' and self.encoding == '7bit':
            mode = 'w'
        else: # encoded parts must be considered as binary
            mode = 'wb'
        f = open(p, mode)
        try: f.write(self.body)
        finally: f.close()
        return p


#-----------------------------------------------------------------------------
#                           U T I L I T I E S
#-----------------------------------------------------------------------------
def dumpMail(msg, path=''):
    ''' Dump mail on file for debug.
        Return: file path.
    '''
    if not path:
        import tempfile
        path =  os.path.join(tempfile.gettempdir(), 'mail_dump.txt')
    
    f = open(path, 'w')
    try:
        for line in msg.lines:
            f.write(line + '\n')
    finally:
        f.close()
    return path

# Trace:
# -----
_log = None         # log file to use
_verbosity = -1     # msg with verbosity > _verbosity are not displayed
_logVerbosity = 100 # "         "           "       "       "  logged

def setLog(newLog):
    global _log
    _log = newLog

def setVerbosity(value):
    global _verbosity
    _verbosity = value

def setLogVerbosity(value):
    global _logVerbosity
    _logVerbosity = value

def trace(msg, msgVerbosity=0):
    ''' Print/log a trace message.

        Msg is printed only if C{msgVerbosity} <= C{_verbosity}.
        
        Msg is written (prefixed with date) into log file (if any) only if
        C{msgVerbosity} <= C{_verbosity}.
        A LF is appended to the message.
    '''
    msg = msg + '\n'
    if msgVerbosity <= _verbosity:
        print msg,
    if _log and msgVerbosity <= _logVerbosity:
        t = time.localtime(time.time())
        date = time.strftime('[%Y/%m/%d %H:%M:%S]', t)
        _log.write('%-6d %s - %s' % (msgVerbosity, date, msg))
        _log.flush()

def _strip2Quotes(s):
    ''' Strip "" around string C{s} if any.
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
def test():
    pass

#-----------------------------------------------------------------------------
#                               M A I N
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    test()
