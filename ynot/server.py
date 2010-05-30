"""WSGI server example"""

import os

#from gevent import wsgi

from ynot import daemon
from ynot import settings
from ynot import templates


basePath = os.path.dirname(
    os.path.dirname(
    os.path.abspath(__file__)
    )
)

EXTENSIONS = [".xhtml", ".shtml", ".html"]


def find(path):
    """
    Attempts to locate a serve the requested
    file

    - if the file exists it simply serves it.
    - elif the file does not exist it checks
       a list of alternate file extensions
    
    """
    result = None
    fp = os.path.join(basePath, path)
    if os.path.exists(fp):
        result = fp
    else:
        p, ext = os.path.splitext(fp)
        for extension in EXTENSIONS:
            np = p + extension
            if os.path.exists(np):
                result = np
    return result


def findAndRender(env, start_response):
    path = env["PATH_INFO"]    
    f = find(path.lstrip("/"))
    if f:
        content = ""
        try:
            contentType = 'text/plain'
            p, ext = os.path.splitext(f)
            if ext in EXTENSIONS:
                content = str(templates.render(f))
                contentType = 'text/html'
            elif ext in [".css"]:
                inputFile = None
                contentType = 'text/css'
                try:
                    inputFile = open(f, "r")
                    content = inputFile.read()
                finally:
                    if inputFile:
                        inputFile.close()
            start_response('200 OK', [('Content-Type', contentType), ('Content-length', str(len(content)))])
        except Exception, e:
            content = str(e)
            start_response('500 Server Error', [('Content-Type', 'text/plain')])
        return [content]
    else:
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return ['Not Found\r\n']


def serve(daemonize=False):
    try:
        if daemonize:
            daemon.daemonize()
        else:
            daemon.makePidFile()
        print 'Serving on %s...'%(settings.PORT,)
        from gevent import wsgi # import occurs after daemonize to avoid broken file descriptors
        server = wsgi.WSGIServer(('', settings.PORT), findAndRender)
        server.serve_forever()
    except StopIteration, e:
        print "Caught StopIteration:", e
    except KeyboardInterrupt, e:
        print "KeyboardInterrupt:", e
    finally:
        print "Shutting down..."
