#readline
import sys
import os
import atexit

try:
    import readline
except ImportError:
    print "Module readline not available."
else:
    import rlcompleter
    readline.parse_and_bind("tab: complete")

histfile = os.path.join(os.environ["HOME"], ".python_history")
try:
    readline.read_history_file(histfile)
except IOError:
    pass

atexit.register(readline.write_history_file, histfile)
del os, histfile
