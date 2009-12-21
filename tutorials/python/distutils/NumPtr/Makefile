# Makes SWIGed Python module 

# Rodrigo Caballero Augi (rca@geosci.uchicago.edu), 
# Department of the Geophysical Sciences, University of Chicago
# 2003


all: setup 

dist:
	python setup.py bdist --formats=gztar,wininst,zip

setup:
	python setup.py build

clean:
	python setup.py clean --all
	rm -rf dist
	rm NumPtr_wrap.c


