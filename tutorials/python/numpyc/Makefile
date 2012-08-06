CC=gcc
PYTHON_INCLUDE=/usr/include/python2.4
PYTHON_LIBRARY=/usr/lib/python2.4

default: myarray.so

myarray.so: mymodule.c
	$(CC) -fPIC -I$(PYTHON_INCLUDE)  -c mymodule.c -o mymodule.o
	$(CC) -shared mymodule.o -o _myarray.so -L$(PYTHON_LIBRARY) -lpython2.4

clean:
	rm mymodule.o
	rm -rf _myarray.so
