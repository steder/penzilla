########################
# Mike Steder
# University of Chicago
# 2005
########################

########################
# *IMPORTANT*
# Look over the following variables.
# Edit the values so that they are appropriate
# for your system.
CC=gcc
# Debugging Options
#CCOPTS=-fPIC -g -Wall -ansi #-pedantic 
# Release Options
CCOPTS=-fPIC -O2
PYTHON=python2.4
PYTHON_INCLUDE=/usr/include/python2.4

# *OPTIONAL*
# Edit these variables to suit your taste:
RM=rm         # command executed to delete make products
CP=cp -rv     # copy command for building tar archive
CD=cd
MV=mv
MKDIR=mkdir      # make directory command for building tar archive
TAR=tar -zcvf     # command for creating a tar archive
BZTAR=tar -jcvf  # command for creating a tar archive
ZIP=zip -r 
NAME=mikempi
MINOR_NUMBER=$(shell svnversion .)
VERSION=1.0a$(MINOR_NUMBER)
ARCHIVE=$(NAME)-$(VERSION)
TARBALL=$(ARCHIVE).tar.gz
BZTARBALL=$(ARCHIVE).tar.bz2
ZIPFILE=$(ARCHIVE).zip
FILES=Makefile *.c *.py *.h SConstruct *.cfg *.txt 
MPI_FILES=mpi/*.py
#
########################

########################
# Do NOT edit variables below this line 
# (It shouldn't be necessary).
LIB=_engine.so
LIBRARIES=-l$(PYTHON)
SRC=$(wildcard *.c)
HEADERS=$(wildcard *.h)
OBJ=$(SRC:.c=.o)
PYBC=$(wildcard *.pyc) $(wildcard mpi/*.pyc)

default: $(LIB)

#$(CC) -Wall -g  -fPIC -I$(PYTHON_INCLUDE)  -c mmpi_module.c -o mmpi_module.o

$(LIB): $(OBJ)
	$(CC) -shared $(OBJ) -o $(LIB) $(LIBRARIES)

test.exe: $(OBJ) 
	$(CC) -o test.exe test.o $(LIBRARIES)

$(OBJ): $(HEADERS)

.SUFFIXES: .o .c

.c.o: 
	$(CC) $(CCOPTS) -I$(PYTHON_INCLUDE) -c $<

clean:
#@echo "I will clean:" $(OBJ) $(LIB) $(PYBC)
	-$(RM) $(OBJ) $(PYBC) $(LIB) test.exe mpi/$(LIB)


distclean:
	-$(RM) dist/*

tar: clean 
	svn export . $(ARCHIVE)
	$(TAR) $(TARBALL) $(ARCHIVE)
	$(RM) -rf $(ARCHIVE)
	$(MV) $(TARBALL) dist
	ln -fs $(TARBALL) dist/$(NAME)-current.tar.gz

bztar: clean 
	svn export . $(ARCHIVE)
	$(BZTAR) $(BZTARBALL) $(ARCHIVE)
	$(RM) -rf $(ARCHIVE)
	$(MV) $(BZTARBALL) dist
	ln -fs $(BZTARBALL) dist/$(NAME)-current.tar.bz2		

zip: clean 
	svn export . $(ARCHIVE)
	$(ZIP) $(ZIPFILE) $(ARCHIVE)
	$(RM) -rf $(ARCHIVE)
	$(MV) $(ZIPFILE) dist
	ln -fs $(ZIPFILE) dist/$(NAME)-current.zip