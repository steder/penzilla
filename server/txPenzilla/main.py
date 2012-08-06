"""
"""
import os

from twisted.internet import reactor
from twisted.python import log
from twisted.python import filepath
from twisted.web import http
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.web.static import File

SITE_DIRECTORY = filepath.FilePath(__file__).parent().sibling("tutorials/")

tutorials = File(SITE_DIRECTORY.path, )

class Error(Resource):
    def __init__(self, path, code):
        Resource.__init__(self)
        print "Error:", path, code
        self.path = path
        self.code = code

    def render_GET(self, request):
        request.setResponseCode(self.code)
        return """
        <html><head>
        <title>%(error)s</title>
        </head>
        <body>
        <h1>%(error)s</h1>
        </body>
        </html>
        """


class TutorialPage(Resource):
    isLeaf = True

    def __init__(self, path):
        Resource.__init__(self)
        print "TutorialPage:", path
        self.path = path
    
    def render_GET(self, request):
        print "TP_GET:", self.path, request
        f = open(self.path,"r")
        return f.read()


class TutorialDirectory(Resource):
    def __init__(self, path):
        Resource.__init__(self)
        print "TutorialDirectory:", path
        self.path = path

    def getChild(self, path, request):
        path = os.path.join(SITE_DIRECTORY, self.path, path)
        print "TD:", path, request
        if os.path.isdir(path):
            return TutorialDirectory(path)
        elif os.path.exists(path):
            return TutorialPage(path)
        else:
            return Resource.getChild(self, path, request)
            

class Root(Resource):
    def __init__(self):
        Resource.__init__(self)
        print "Root init"

    def getChild(self, path, request):
        path = os.path.join(SITE_DIRECTORY.path, path)
        print "Root:", path, request
        if os.path.isdir(path):
            return TutorialDirectory(path)
        elif os.path.exists(path):
            return TutorialPage(path)
        else:
            return Resource.getChild(self, path, request)


if __name__=="__main__":
    print "Starting to monitor %s:"%(SITE_DIRECTORY,)
    root = Root()
    factory = Site(root)
    reactor.listenTCP(8880, factory)
    reactor.run()
