PYTHONINCLUDEDIR=/usr/include/python2.3

all: mpimodule.so

mpimodule.so:
	gcc -shared -I$(PYTHONINCLUDEDIR) mpimodule.c -o $@

clean:
	rm -f *.o mpimodule.so