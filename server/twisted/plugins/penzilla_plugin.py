import sys

from zope import interface

from twisted import plugin
from twisted.application import service
from twisted.python import usage

from bacon import server, settings


class Options(usage.Options):
    optParameters = (
        ('config', 'c', None, 'Config file'),
        ('port', 'p', None, 'Port on which to listen.'),
    )


class BaconServiceMaker(object):
    interface.implements(plugin.IPlugin, service.IServiceMaker)
    description = "Delicious"
    options = Options
    tapname = 'bacon'

    def makeService(self, options):
        """
        Return an instance of bacon.server.BaconServer
        """
        config_file = "bacon.conf"
        if options['config'] is not None:
            config_file = options['config']

        try:
            settings.load(config_file)
        except settings.BaconSettingsError, e:
            print "Unable to load configuration file: %s"%(config_file,)
            print "Please confirm that %s exists and is a valid yaml file."%(config_file,)
            print settings.__doc__
            sys.exit()
            
        port = settings.PORT

        if options['port'] is not None:
            port = int(options['port'])

        return server.BaconServer(port)


serviceMaker = BaconServiceMaker()
