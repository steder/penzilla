# Mike Steder
# 10/29/03
#
# This is what I'm doing instead of studying or homework
# :~)
"""
This is a script designed to do some simple analysis of
the CS373 Grade's.
  Average Score Per Assignment
  Average Overall
  High Score
  Low Score

  Grade Ranges assuming one standard deviation from the average
  set's the curve.

  If given a student Alias it returns:
    *all these statistic's
    *The student's projected letter grade

  A CGI Frontend would be awesome!
"""
import sys
import os
import string

"""
This returns a dictionary of lists:
data = {'alias1':[hw0, hw1, ..., midterm]}
"""
def parse(filename):
    data = {}
    infile = open(filename,"r")
    header = infile.readline()
    header = header.split("\t")
    # Parse the rest of the file:
    lcount = 0
    file = infile.readlines()
    for line in file:
        line = line.split("\t")
        if len(line) != len(header):
            print "Ignoring line!(",lcount,"):", string.join(line,"\t")
            continue
        alias = line[0]
        # Convert all the scores to floats
        for i in range(len(line[1:])):
            try:
                line[i+1] = string.atof(line[i+1])
            except ValueError:
                line[i+1] = 0.0
        data[alias] = line[1:]
        lcount = lcount + 1
    return data,header

"""
Stat's Consist of the following:
average for each category
average of total points
"""
def getaverages(data,header):
    names = data.keys()
    grades = []
    for i in range(len(header)-1):
        grades.append(0)
        for name in names:
            grades[i] += data[name][i]
        grades[i] = grades[i] / (len(names) * 1.0)  
    return grades


def tentative(data, header, name):
    try:
        grades = data[name]
    except KeyError:
        print "Keys are case sensitive:",name,"does not exist (as typed)!"
        return "Keys are case sensitive:",name,"does not exist (as typed)!"
    sum = 0
    for i in grades[:-1]:
        sum += i
    print sum, grades[-1]
    percent = ((0.37 * sum)/160.0)+((0.67 * grades[-1])/90.0)
    return percent

"""
Let's generate a basic html table with all this info in it.
"""
def html_header():
    html = "<html>\n"+\
           "<title>CS373 Grades</title>"+\
           "<h1>CS373 Grades</h1>"
    return html

def html_footer():
    html = "</html>\n"
    return html

def htmllize(data,tableheader):
    body = html_header()
    body += "<table>\n"+\
           "<tbody>\n"
    line = "<tr><b>"
    line += "<td width=\"10%\"><b>"+tableheader[0]+"</b></td>"
    for item in tableheader[1:]:
        line += "<td width=\"15%\"><b>"+item+"</b></td>"
    line += "</b></tr>\n"
    body += line
    names = data.keys()
    names.sort()
    for name in names:
        scores = data[name]
        line = "<tr><td width=\"10%\">"+name+"</td>"
        for score in scores:
            line += "<td width=\"15%\">"+str(score)+"</td>"
        line += "</tr>"+"\n"
        body += line
    body += html_averages(getaverages(data,tableheader))
    body += "</tbody>\n"+\
            "</table>\n"
    body += html_footer()
    return body

def html_averages(averages):
    html = "<tr><td width=\"10%\"><b>"+"Average:"+"</b></td>"
    for item in averages:
        html += "<td width=\"15%\">"+str(item)+"</td>"
    html += "\n"
    return html

instructions = "usage:  python grade.py grades.txt"
if __name__=="__main__":
    if len(sys.argv) == 2:
        if os.path.isfile(sys.argv[1]):
            data,header = parse(sys.argv[1])
            html = htmllize(data,header)
            print html
            outfile = open("grades.html","w")
            outfile.write(html)
            outfile.close()
        else:
            print instructions
    elif len(sys.argv)==3:
        if os.path.isfile(sys.argv[1]):
            data,header = parse(sys.argv[1])
            estgrade = tentative(data, header, sys.argv[2])
            print estgrade
        else:
            print instructions
    else:
        print instructions
