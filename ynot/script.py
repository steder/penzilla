"""
ynot - simple wsgi server for Penzilla tutorial content

Usage:

    $ ynot

Options:

    $ ynot --help
    $ ynot --daemon

"""

import sys

from ynot import server

def main():
    daemonize = False
    if len(sys.argv) > 1:
        if "--daemon" in sys.argv:
            daemonize = True
        if "--help" in sys.argv:
            print __doc__
    server.serve(daemonize)

