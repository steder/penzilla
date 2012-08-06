import cgi, sys, string
import gradelib
form = cgi.FieldStorage() # parse form data
print "Cotent-type: text/html"

html = """
<html>
<title>CS373: Unofficial Grade info for: %(alias)</title>
<body>
<h1>CS373: Unofficial Grade info for: %(alias)</h1>
<table>
<tbody>
%(classdata)
</tbody>
</table>
<P>
%(scale)
<h4>
%(tentative)
</h4>
</body>
</html>"""

data = {}
classdata = gradelib.parse("grades.txt")
htmldata = gradelib.htmlize(classdata)
if not form.has_key("alias"):
    data["alias"] = "(unknown)"
else:
    data["alias"] = form["alias"].value
    
temp = gradelib.tentative(classdata[0],classdata[1],form["alias"].value)


""" 
[78,100]  -->  A       
[60,78)   -->  B
       (42,60)   -->  C
       (25,42]   -->  D
       [0,25]    -->  F
"""
data["scale"] ="""
<ul> 
[78,100]  -->  A       
[60,78)   -->  B       
(42,60)   -->  C
(25,42]   -->  D
[0,25]    -->  F
</ul>""" 

if temp >= 78:
    data["tentative"]="You have",temp,"percent"+\
                       "so you are currently getting an A"
elif 60 < temp < 78:
    data["tentative"]="You have",temp,"percent"+\
                       "so you are currently getting an A"
elif 42 < temp < 60:
    data["tentative"]="You have",temp,"percent"+\
                       "so you are currently getting an A"
elif 25 < temp <= 42:
    data["tentative"]="You have",temp,"percent"+\
                       "so you are currently getting an A"
elif 0 <= temp <= 25:
    data["tentative"]="You have",temp,"percent"+\
                       "so you are currently getting an A"
    
print html % data
