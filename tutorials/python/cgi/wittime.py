#!/usr/bin/python
import cgitb
cgitb.enable()

print "Content-type: text/html"
print

import time

print "<HTML>"
print "<HEAD>"
print "<TITLE>Penzilla.net:  What is the Time? Example</TITLE>"
print "</HEAD>"
print "<BODY>"
print "<H2>Penzilla.net What is the Time?(wittime.py) Example:</h2>"
print "<P>Penzilla thinks that it is: %s</P>" % time.ctime()
print "</BODY>"
print "</HTML>"
