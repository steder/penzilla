"""WSGI server example"""

import os

#from gevent import wsgi

from ynot import daemon
from ynot import templates


basePath = os.path.dirname(
    os.path.dirname(
    os.path.abspath(__file__)
    )
)


def find(path):
    p = os.path.join(basePath, path)
    if not os.path.exists(p):
        p = None
    return p


def findAndRender(env, start_response):
    path = env["PATH_INFO"]    
    f = find(path.lstrip("/"))
    if f:
        content = ""
        try:
            content = str(templates.render(f))
            start_response('200 OK', [('Content-Type', 'text/html')])
        except Exception, e:
            content = str(e)
            start_response('500 Server Error', [('Content-Type', 'text/plain')])
        return [content]
    else:
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return ['Not Found\r\n']


def serve(daemonize=False):
    print 'Serving on 8088...'
    try:
        if daemonize:
            daemon.daemonize()
        else:
            daemon.makePidFile()
        from gevent import wsgi # import occurs after daemonize to avoid broken file descriptors
        server = wsgi.WSGIServer(('', 8088), findAndRender)
        server.serve_forever()
    except KeyboardInterrupt, e:
        print "Shutting down..."
        print e
