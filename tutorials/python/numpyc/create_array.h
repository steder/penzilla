#include <Python.h>
#include <Numeric/arrayobject.h>

#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>

/* This function takes 1 argument, N, and creates a 1D array of that size 
   and returns it to python with it's values initialized with 0 to N-1. */
static PyObject *create_array(PyObject * self, PyObject * args)
{
    int N, i;
    PyArrayObject *result;
    int dimensions[1];
    int *buffer;

    if (!PyArg_ParseTuple(args, "i", &N))
    {
      return NULL;
    }
    dimensions[0] = N;
    result = (PyArrayObject *) PyArray_FromDims(1, dimensions, PyArray_INT);
    
    buffer = result->data;
    for( i = 0; i < N; i++ ) 
    {
      buffer[i] = i; 
    }

    return PyArray_Return(result);
}
