#include <Python.h>
#include <Numeric/arrayobject.h>
#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>

#define IDENTITY_DOC "\
This method simply unpacks the Array (so that it could be modified)\
and then returns it unchanged."
static PyObject *identity(PyObject *self, PyObject *args)
{
int i,n;
PyObject *input;
PyArrayObject *array;
char *aptr;

 if (!PyArg_ParseTuple(args, "O", &input ))
   return NULL;
 array = (PyArrayObject *) PyArray_ContiguousFromObject(input, PyArray_INT, 0, 3);
 if (array == NULL)
   return NULL;
 
 // Compute Size of Array 
 if(array->nd == 0)
   n = 1;
 else {
   n = 1;
   for(i=0;i<array->nd;i++) 
     n = n * array->dimensions[i];
 } 
 
 aptr=(char*)(array->data);
 
 // Do Your Array Operation(s)

 // Return the result
 return PyArray_Return(array);
}



