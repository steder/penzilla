#include <Python.h>
#include <Numeric/arrayobject.h>

#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>


static PyObject *pyError;

/*
static PyObject *identity(PyObject * self, PyObject * args);
static PyObject *create_array(PyObject * self, PyObject * args);
*/
#include "identity.h"
#include "create_array.h"

static PyMethodDef myMethods[] = {
    {"identity",		identity,			METH_VARARGS,     	IDENTITY_DOC},
    {"create_array", create_array, METH_VARARGS,          "create_array"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


void init_myarray(void)
{
	PyObject *m;
    PyObject *tmp;
	import_array();
	m=Py_InitModule("_myarray", myMethods);
	pyError = PyErr_NewException("myarray.error", NULL, NULL);
    Py_INCREF(pyError);
    PyModule_AddObject(m, "error", pyError);
}

