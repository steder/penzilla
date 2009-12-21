#!/usr/bin/python
# For CGI support
import cgi
# For debugging support
import cgitb; cgitb.enable()

# import needed libraries:
import sys,random

# This needs to be here first.
print "Content-Type: text/html"     # Just set the standard html content type.
print                               # Blank line signifies the end of the header info.

print "<title>Rock Paper Scissors Spock Lizard:  The Challenge</title>"
print "<body>"
print "<h1>Rock Paper Scissors Spock Lizard</h1>"

form = cgi.FieldStorage()

if not form.has_key("choice"):
    print "<P><b>"
    print "Please go back and choose a throw so we can play a game."
    print "</b></p>"
    sys.exit(1)

## A list of image links:
images = ['<img src="http://www.penzilla.net/tutorials/python/cgi/rock.jpeg">',
          '<img src="http://www.penzilla.net/tutorials/python/cgi/paper.jpeg">',
          '<img src="http://www.penzilla.net/tutorials/python/cgi/scissors.jpeg">',
          '<img src="http://www.penzilla.net/tutorials/python/cgi/spock.jpeg">',
          '<img src="http://www.penzilla.net/tutorials/python/cgi/lizard.jpeg">']

## Now, generate my choice:
# 0 = Rock
# 1 = Paper
# 2 = Scissors
# 3 = Spock
# 4 = Lizard
comp = (random.randint(0,255)) % 5
user = int(form.getvalue("choice","")) % 5

## Compute a winner:
#Scissors cuts Paper covers Rock crushes Lizard poisons Spock smashes
#Scissors decapitates Lizard eats Paper disproves Spock vaporizes Rock
#crushes Scissors.

winner = -1 # Computer = 0, Player = 1
message = ""
if comp == user: # TIE
    message = "Tie!"
elif comp == 0:  # Comp = Rock
    if user == 1: 
        winner = 1
        message = "Paper covers Rock"
    if user == 2:
        winner = 0
        message = "Rock crushes Scissors"
    if user == 3:
        winner = 1
        message = "Spock vaporizes Rock"
    if user == 4:
        winner = 0
        message = "Rock crushes Lizard"
elif comp == 1:  # Comp = Paper
    if user == 0: 
        winner = 0
        message = "Paper covers Rock"
    if user == 2:
        winner = 1
        message = "Scissors cuts Paper"
    if user == 3:
        winner = 0
        message = "Paper disproves Spock"
    if user == 4:
        winner = 1
        message = "Lizard eats Paper"
elif comp == 2:  # Comp = Scissors
    if user == 0: 
        winner = 1
        message = "Rock crushes Scissors"
    if user == 1:
        winner = 0
        message = "Scissors cuts Paper"
    if user == 3:
        winner = 1
        message = "Spock smashes Scissors"
    if user == 4:
        winner = 0
        message = "Scissors decapitates Lizard"
elif comp == 3:  # Comp = Spock
    if user == 0: 
        winner = 0
        message = "Spock vaporizes Rock"
    if user == 1:
        winner = 1
        message = "Paper disproves Spock"
    if user == 2:
        winner = 0
        message = "Spock smashes Scissors"
    if user == 4:
        winner = 1
        message = "Lizard poisons Spock"
elif comp == 4:  # Comp = Lizard
    if user == 0: 
        winner = 1
        message = "Rock crushes Lizard"
    if user == 1:
        winner = 0
        message = "Lizard eats Paper"
    if user == 2:
        winner = 1
        message = "Scissors decapitate Lizard"
    if user == 3:
        winner = 0
        message = "Lizard poisons Spock"

## Time to Lay out the HTML Results Page
if user == 0:
    userstr = "Rock"
elif user == 1:
    userstr = "Paper"
elif user == 2:
    userstr = "Scissors"
elif user == 3:
    userstr = "Spock"
elif user == 4:
    userstr = "Lizard"
if comp == 0:
    compstr = "Rock"
elif comp == 1:
    compstr = "Paper"
elif comp == 2:
    compstr = "Scissors"
elif comp == 3:
    compstr = "Spock"
elif comp == 4:
    compstr = "Lizard"

print "<H2>",userstr, "<font color='red'>versus</font>", compstr, "</H2>"

## A table to present the result pictures
print "<table>"
print "  <caption></caption>"
print "  <tbody>"
print "    <tr>"
print "      <td>",images[user],"</td>"
print "      <td>","<font color='green'>",message,"</font>","</td>"
print "      <td>",images[comp],"</td>"
print "    </tr>"
print "  </tbody>"
print "</table>"

# Print the result message:
if winner == -1:
    print "<h2><font color='green'>You Tied!</font></h2>"
elif winner == 1:
    print "<h2><font color='blue'>You Win!</font></h2>"
else:
    print "<h2><font color='red'>You Lose!</font></h2>"

print "<h2>Again?</h2>"
print '<FORM action="http://www.penzilla.net/cgi-bin/rpssl.py" method="GET" enctype="application/x-www-form-urlencoded">'
print "<b>"
print 'Rock<INPUT type="radio" name="choice" value="0"><br>'
print 'Paper<INPUT type="radio" name="choice" value="1"><br>'
print 'Scissors<INPUT type="radio" name="choice" value="2"><br>'
print 'Spock<INPUT type="radio" name="choice" value="3"><br>'
print 'Lizard<INPUT type="radio" name="choice" value="4"><br>'
print "</b>"
print '<INPUT type="submit" name="submit" value="Throw">'
print "</FORM>"
