"""
build.py

Generates pygmentized versions of any python files whose corresponding .py.html
file is out of date.
"""


import os

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


ROOT_DIR = "."

lexer = get_lexer_by_name("python", stripall=True)
formatter = HtmlFormatter(linenos=False, cssclass="syntax")


def highlightFile(inputPath, outputPath):
    i = open(inputPath, "r")
    o = open(outputPath, "w")
    code = i.read()
    highlight(code, lexer, formatter, o)
    

for dirpath, dirnames, filenames in os.walk(ROOT_DIR):
    for filename in filenames:
        basename, ext = os.path.splitext(filename)
        if ext == ".py":
            pyPath = os.path.join(dirpath, filename)
            htmlPath = pyPath + ".html"
            if os.path.exists(htmlPath):
                pyStat = os.stat(pyPath)
                htmlStat = os.stat(htmlPath)
                if pyStat.st_mtime > htmlStat.st_mtime:
                    print "Updating %s -> %s"%(pyPath, htmlPath)
                    highlightFile(pyPath, htmlPath)
            else:
                print "Creating %s -> %s"%(pyPath, htmlPath)
                highlightFile(pyPath, htmlPath)
