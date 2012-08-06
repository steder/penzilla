currentdir = $(shell pwd)
py2html = python ${currentdir}/txt2html/py2html.py
# Paths to various files to py2html-ize
files = ${currentdir}/*/*.py
cruft = ${currentdir}/*/*.py.html
# Base archive name:
archivename = Archives/python_tutorial
archivedir = this
all : pytml 

pytml :
	${py2html} ${files}

mime-types:
	svn pset svn:mime-type text/html *.html
	svn pset svn:mime-type text/html */*.html

clean : 
	-rm ${cruft}
