#!/usr/bin/env python
#---------------------------------------------------------------------------
# dataxfer.py               Data transfer utilities
#
# See __doc__ string below.
#
# Requires:
#    - Python 2.0 or newer (www.python.org)
#    - platform.py (http://starship.skyport.net/~lemburg/platform.py)
#    - OS: portable
#
# TODO:
#   - verbose mode
#   - delete uploaded files on FTP server (in retrieveData) ??
#   - binary and text modes.
#   x cache FTP connection.
#
# $Id: //depot/rgutils/rgutils/dataxfer.py#1 $
#---------------------------------------------------------------------------
'''
Functions for transfering arbitrary sized data in a distributed
(client/server) environment.

Typical use is for passing a big amount of data as an argument to a
remote call. Instead of passing the data itself as an arg, you should
call L{prepareData}(data,...) and pass the returned I{data handle} instead.
The handle is later converted back to the original data by calling
L{retrieveData}(handle,...).

Internally, data is passed "as is" in the handle if its size is less
than a given threshold (option), otherwise it is gzipped, uploaded to
a FTP server and the URL is passed in the handle.
Source data my be passed to prepareData as a string or as a path of
a file containing the data. Likewise, data may be retrieved as a string
or as a local file, INDEPENDENTLY of the way it was passed to
L{prepareData}(), e.g.:

B{client}::
    import dataxfer
    # Data is a string
    dh = dataxfer.prepareData(stringData, storeThreshold=10000)
    == OR ==
    # Data is in a file
    fh = dataxfer.prepareData(filePath, isFilePath=true, 
                              storeThreshold=10000)
    server.foo(dh, otherArgs...)

B{server}::
    import dataxfer
    def foo(self, dh, otherArgs...):
        # Retrieve data as a string:
        data = dataxfer.retrieveData(dh)
        == OR ==
        # Retrieve data at a temp local path:
        fDataPath = dataxfer.retrieveData(dh, filePath='')
        # Retrieve data at a specified local path:
            dataxfer.retrieveData(dh, filePath='myDir/myFile')
'''
__version__ = '1.0.' + '$Revision: #1 $'[12:-2]
__author__ = 'Richard Gruet', 'rjgruet@yahoo.com'
__date__    = '$Date: 2003/05/23 $'[7:-2], '$Author: rgruet $'[9:-2]
__since__ = '2000-10-11'
__doc__ += '\n@author: %s (U{%s})\n@version: %s' % (__author__[0],
                                            __author__[1], __version__)

import os, sys, string, re, time
import gzip, tempfile, urlparse, ftplib, cStringIO
import platform # M.A. Lemburg's utility

true, false = -1, 0
MAGIC = '21121957'  # Magic number for data handles.


#------------------------------------------------------------------------------
def prepareData(data, isFilePath=false, **options):
#------------------------------------------------------------------------------
    '''
    Prepares the given string or file for transfer.

    Returns a string representing a "handle" to be used with the function
    retrieveData to retrieve the data.
    If data size is < C{storeThreshold}, this handle is simply the data
    itself, uncompressed.
    Otherwise, the "handle" is the FTP URL of a gzipped file containing the compressed data.

    B{Header:}

    In both case, the handle also contains a header with meta information, so
    you B{must} always use L{retrieveData()} to retrieve the data. 
    The header is a single LF terminated line containing a comma separated
    unordered list of keywords among:

        - C{magic}=L{MAGIC}       -- identifies a dataxfer handle
        - C{type}={data|url}      -- handle either directly contains data, or the
                                FTP URL of a file containing data.
        - C{filename}=I{basename} -- base name of original file if known.
        - C{compresslevel}=1-9    -- The gzip compression level used if data
                              transfered via FTP.
        - C{sent-by}==I{hostName}  -- the hostname of the caller
        - C{sent-on}=YYYYMMDDHHMMSS -- Send GMT date+time.


    @param data: [string] The data to transfer or the path of a B{local} file
                containing that data, according to C{isFilePath}.
    @param isFilePath: [boolean] Determines whether C{data} represents a
                       file path or directly the data.
    @param options: Keyword options:
        - C{compressLevel} [1-9, default:9] --  1:fastest, low compression;
                                             9:slowest, best compression
        - C{storeThreshold} -- Above this size (in bytes), the data will be uploaded
                to a FTP server and its URL returned. Set threshold to 0 if you
                want to ALWAYS transfer via FTP [default: 2000000]
        - C{ftpHost}  -- IP address of the FTP server to use if store is needed.
                Defaults to envt var DATAXFR_FTP if it exists, 'localhost'
                otherwise.
        - C{ftpDir}  -- Relative directory on the FTP server where to upload
                  the gzipped file [default: 'corba-tmp']
        - C{ftpUser}, C{ftpPasswd} -- User name and password to use for the FTP
                  connection [default: 'corba', 'corba']
        - C{ftpBlkSize} -- Size of transfer blocks in bytes [default: 8192]

    @return: [string] The data transfer "handle" to pass to the remote call.
            It is either the data itself (if size < threshold), or the FTP
            URL of the gzipped file (to be downloaded).
    @see: L{retrieveData}()
    '''
    header = [
              'magic=%s' % MAGIC,
              'sent-on=%s' % time.strftime('%Y%m%d%H%M%S',
                                            time.gmtime(time.time())),
              'sent-by=%s' % platform.node()
             ]
    
    # Determine transfer method according to data size:
    if isFilePath:
        size = os.path.getsize(data)
        header.append('filename=%s' % os.path.basename(data))
    else:
        size = len(data)
    
    storeThreshold = options.get('storeThreshold', 2000000)
    if storeThreshold <= 0 or size >= storeThreshold:
        
        # Compress data:
        compressLevel = options.get('compressLevel', 9)
        header.extend(['type=url', 'compresslevel=%d' % compressLevel])
        
        if not isFilePath:
            f = cStringIO.StringIO(data)
        else:
            f = open(data, 'rb')
        
        gzPath = tempfile.mktemp('.gz')
        z = gzip.open(gzPath, 'wb', compressLevel)
        try:
            while true:
                s = f.read(100000)
                if not s:
                    break
                z.write(s)
        finally:
            z.close()   # required to flush!
            f.close()
        
        # Upload gzipped file to the FTP server:
        try:
            try:
                ftpHost = options['ftpHost']
            except KeyError:
                ftpHost = os.environ.get('DATAXFR_FTP', 'localhost')

            ftpDir = options.get('ftpDir', 'corba-tmp')
            if ftpDir[0] == '/':        # path must be relative for ftp
                ftpDir = ftpDir[1:]
            if ftpDir[-1] == '/':
                ftpDir = ftpDir[:-1]
            uploadPath = '%s/%s' % (ftpDir, os.path.basename(gzPath))
            url = 'ftp://%s/%s' % (ftpHost, uploadPath)

            try:
                ftpUser = options.get('ftpUser', 'corba')
                ftpPasswd = options.get('ftpPasswd', 'corba')
                ftp = _FTPLog(ftpHost, ftpUser, ftpPasswd)
            except:
                t, v, tb = sys.exc_info()   #(old-style string exceptions!)
                raise Exception('Cannot connect or log to FTP server "%s" as '
                        'user %s (%s): %s' % (ftpHost, ftpUser, ftpPasswd, v))
            try:
                ftp.storbinary('STOR %s' % uploadPath, open(gzPath, 'rb'),
                                options.get('ftpBlkSize', 8192))
                _FTPClose(ftp)
            except:
                t, v, tb = sys.exc_info()
                raise Exception("can't upload %s to %s: %s" % (gzPath, url, v))
            dataHandle = '%s\n%s' % (string.join(header, ','), url)
        finally:
            os.remove(gzPath)

    else:   # [data size < threshold]
        header.append('type=data')
        header = string.join(header, ',') + '\n'
        if isFilePath:
            dataHandle = header + open(data, 'rb').read()
        else:
            dataHandle = header + data

    return dataHandle   

#------------------------------------------------------------------------------
def retrieveData(dataHandle, **options):
#------------------------------------------------------------------------------
    '''
    Retrieves data transfered from a data transfer "handle".
    
    Given a "data transfer handle" produced by L{prepareData}, this
    function retrieves the data as a string or a local file.

    @param dataHandle: The data "handle" produced by L{prepareData()}.
    @param options: Keyword options:
        - C{localPath} -- if specified, store data as a file at given path;
                        if localPath='', store data in directory C{localDir}
                        (see below) with an automatically assigned name.
                        if not specified, data is returned as a mere string.
        - C{localDir} -- Local directory where to create the local file (if.
                        [default is $TEMP directory]
        - C{ftpUser}, C{ftpPasswd} -- User name and password to use for the FTP
                        connection [default: 'corba', 'corba']
        - C{ftpBlkSize} -- Size of transfer blocks in bytes [default: 8192]

    @return: The data transfered, or the path of a local file containing
            that data, depending if option C{localPath} specified or not.
    @see: L{prepareData()}
    ''' 
    # Parse header (first line):
    i = string.find(dataHandle, '\n')
    if i == -1:
        raise Exception("Can't find header in data handle.")
    header = dataHandle[:i]
    body = dataHandle[i+1:]
    
    kw = {}
    for name, value in re.findall(r'([\w\-_]+)[ \t]*=[ \t]*([\w\-_]+)',
                                                                header):
        kw[string.lower(name)] = value

    magic = kw.get('magic', '')
    if magic != MAGIC:
        raise Exception("Invalid data handle (bad magic number).")
    
    typ = kw.get('type', '')
    if typ not in ('url', 'data'):
        raise Exception('No type or invalid type info ("%s") in header.' % t)
    
    fileName = kw.get('filename', '')
    
    # If we must store on file, compute local path:
    storeAsFile = options.has_key('localPath')
    if storeAsFile:
        localPath = options['localPath']
        if not localPath:       
            localDir = options.get('localDir', tempfile.gettempdir())
            if fileName:
                localPath = os.path.join(localDir, fileName)
            else:
                localPath = os.path.join(localDir, tempfile.gettempprefix())
    
    # Retrieve data :
    if typ == 'data':
        if storeAsFile:
            open(localPath, 'wb').write(body)
            r = localPath
        else:
            r = body
        
    else:
        # [typ=='url'] Download the gzipped data into a temporary file:
        url = body
        gzPath = tempfile.mktemp('.gz')
        scheme,ftpHost, path, parms, query, frag = urlparse.urlparse(url)
        if scheme != 'ftp' or not ftpHost or not path:
            raise Exception('Not a legal FTP URL: "%s".' % url)
    
        try:
            ftpUser = options.get('ftpUser', 'corba')
            ftpPasswd = options.get('ftpPasswd', 'corba')
            ftp = _FTPLog(ftpHost, ftpUser, ftpPasswd)
        except:
            t, v, tb = sys.exc_info()   #(old-style string exceptions!)
            raise Exception('Cannot connect or log to FTP server "%s" as '
                    'user %s (%s): %s' % (ftpHost, ftpUser, ftpPasswd, v))
    
        path = path[1:]     # avoid '/', path must be relative for ftp
        try:
            ftp.retrbinary('RETR %s' % path, open(gzPath, 'wb').write,
                            options.get('ftpBlkSize', 8192))
            _FTPClose(ftp)
        except:
            t, v, tb = sys.exc_info()
            raise Exception("Can't download %s to %s: %s" % (url, gzPath, v))
    
        # Unzip data into a string or a local file (preferably the one
        # indicated, if any):
        z = gzip.open(gzPath, 'rb')
        try:
            if storeAsFile:
                f = open(localPath, 'wb')
                try:
                    while true:
                        s = z.read(100000)
                        if not s:
                            break
                        f.write(s)
                finally:
                    f.close()
                r = localPath
            else:
                r = z.read()
        finally:
            z.close()

    return r        
    
#------------------------------------------------------------------------------
#                           P R I V A T E
#------------------------------------------------------------------------------

_ftpCache = {} # FTP cache { (host, user, passwd): FTP object,..}

def _FTPLog(host, user, passwd, useCache=true):
    ''' Connects to a FTP server.
    
        Transparently uses cached connections.
        @param host: FTP host address
        @param user: Login user name 
        @param passwd: User password
        @param useCache: If true use cached connections
        @return: A ftplib.FTP instance
    '''
    ftp = None
    if useCache:
        global _ftpCache
        try:
            ftp = _ftpCache[host, user, passwd]
        except KeyError:
            pass
        else:
            try:
                ftp.pwd()       # check timeout
            except:
                ftp = None
    
    if not ftp:
        #print '_FTPLog: not in cache, must connect' ##
        ftp = _ftpCache[host, user, passwd] = ftplib.FTP(host)
        ftp.login(user, passwd)
    else:
        pass #print 'Use cached connection' ##
    
    return ftp
    

def _FTPClose(ftp):
    ''' Disconnect from a FTP server.
    
        Disconnection is not actually performed since we cache
        the connections for later use.
        
        @param ftp: [ftplib.FTP] 
    '''
    pass

#------------------------------------------------------------------------------
def tests():
#------------------------------------------------------------------------------
    ''' Module self-tests.
    '''
    print 'Testing dataxfer...'
    # Generate our own test file:
    fPath = tempfile.mktemp()
    testString = 'Corba is good for you, folks! ' * 1000
    f = open(fPath, 'w')
    f.write(testString)
    f.close()
    try:
        _test(testString, fPath, 'string', 'string', false)
        _test(testString, fPath, 'string', 'string', true)
        _test(testString, fPath, 'string', 'file', false)
        _test(testString, fPath, 'string', 'file', true)
        _test(testString, fPath, 'file', 'string', false)
        _test(testString, fPath, 'file', 'string', true)
        _test(testString, fPath, 'file', 'file', false)
        _test(testString, fPath, 'file', 'file', true)
        
        print 'Performing 10 x transfers via FTP...'
        t0 = time.time()
        for i in range(10):
            _test(testString, fPath, 'string', 'string', true)
        print 'done in %.2f sec.' % (time.time() - t0)
            
    finally:
        os.remove(fPath)
    
    print '=> tests passed.'

_testNo = 0

def _test(testString, fPath, src, dst, ftp):
    global _testNo
    _testNo = _testNo + 1
    isFilePath = (src == 'file')
    if ftp:
        s = 'FTP/compressed'
        storeThreshold=0
    else:
        s = 'uncompressed'
        storeThreshold=2000000
    print 'Test #%d: %s to %s, %s...' % (_testNo, src, dst, s)
    if isFilePath: data = fPath
    else: data = testString
    dh = prepareData(data, isFilePath, storeThreshold=storeThreshold)
    if dst == 'file':
        path = retrieveData(dh, localPath='')
        try:
            gotString = open(path).read()
        finally:
            os.remove(path)
    else:
        gotString = retrieveData(dh)
    
    if gotString != testString:
        raise Exception('test failed.')
    else:
        print 'OK'
    
#------------------------------------------------------------------------------
#                           M  A  I  N
#------------------------------------------------------------------------------
if __name__ == '__main__':
    tests()
    