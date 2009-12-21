"""
"""
from twisted.internet import reactor
from twisted.python import log
from twisted.python import filepath
from twisted.web import http
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.web.static import File

TUTORIALS_DIRECTORY = filepath.FilePath(__file__).parent().sibling("tutorials/")

tutorials = File(TUTORIALS_DIRECTORY.path, )

class Error(Resource):
    def __init__(self, path, code):
        Resource.__init__(self)
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
        self.path = path
    
    def render_GET(self, request):
        return """
        <html>
        <body>
        %s
        </body>
        </html>
        """ %(self.path,)


class TutorialDirectory(Resource):
    def __init__(self, path):
        Resource.__init__(self)
        self.path = path

    def getChild(self, path, request):
        if 


class Root(Resource):
    def __init__(self):
        Resource.__init__(self)

    def getChild(self, path, request):
        if path.lower().endswith("shtml"):
            return TutorialPage(path)
        else:
            return TutorialDirectory(path)
        else:
            return Error(path, http.NOT_FOUND)


if __name__=="__main__":
    print "Starting to monitor %s:"%(TUTORIALS_DIRECTORY,)
    root = Root()
    factory = Site(root)
    reactor.listenTCP(8880, factory)
    reactor.run()
