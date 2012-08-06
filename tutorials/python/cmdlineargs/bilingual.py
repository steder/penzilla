# bilingual.py
"""
Please excuse my highschool german! :~)
"""
import sys

if (len(sys.argv) > 1):
    if( sys.argv[1] == 'english' ):
        print "Hello World!"
    elif( sys.argv[1] == 'german' ):
        print "Guten Tag Welt!"
    else:
        print "Which language?"
        print "Welche sprache?"
else:
    print "Which language do you want?"
    print "Welch sprache wisst du?"
