/*
 * Mike Steder
  * 2005
 */

/* Standard Header files */
#include <Python.h>
#include <Numeric/arrayobject.h>
#include <stdio.h>
#include <stdlib.h>

static PyObject *count_neighbors(PyObject * self, PyObject * args);

/* Definitions */


static PyObject *createFreeNeighbor( int x, int y )
{
  PyObject *tmp;
  tmp = PyTuple_New(2);
  if( tmp == NULL )
    return NULL;
  PyTuple_SET_ITEM( tmp, 0, PyInt_FromLong( x ) );
  PyTuple_SET_ITEM( tmp, 1, PyInt_FromLong( y ) );
  return tmp;
}

static PyObject *count_neighbors(PyObject * self, PyObject * args)
{
  /* int NumberOfNeighbors, pylist FreeSpaces = 
                                                              count_neighbors( int x, int y, 2d int array );
  */
  int i, j;
  int x,y, ni, nj, nx, ny;
  int num_neighbors = 0;
  PyObject *list;
  PyObject *tmp;
  PyObject *input;
  PyArrayObject *array;
  int *grid;
    
    if (!PyArg_ParseTuple
        (args, "iiO", &x, &y, &input)) {
      return NULL;
    }
    array = (PyArrayObject *) PyArray_ContiguousFromObject(input,PyArray_INT, 2, 2);
    if (array == NULL)
      return NULL;
    
    /* our list of free neighbors */
    list = PyList_New(0);
    if (list == NULL)
      return NULL;

    /* dimensions of array */
    ni = array->dimensions[0];
    nj = array->dimensions[1];
    
    grid = (int *)(array->data);
    /*printf("x,y,ni, nj = %d,%d,%d,%d\n",x,y,ni,nj);*/
    /* actual count neighbors code */
    for( i = -1; i <= 1; i++ ) {
      for( j = -1; j <= 1; j++ ) {
        /* These bizarre modulo operations
             are bizarre because I need them to give the same
             values python returns for the modulus of a negative number.
         */
        nx = (ni+(x+i))%ni;
        ny = (nj+(y+j))%nj;
        if( grid[(nx*nj) + ny] == 1 ) {
          if( (nx != x) || (ny != y) ) {
            num_neighbors += 1;
          }
        }
        else {
          PyList_Append( list, createFreeNeighbor( i, j ) );
        }
      }
    }
    return Py_BuildValue("(iO)", num_neighbors, list );
}

/* 
   A list of all methods to be included in "_mpi"
   
   Acceptable values for the 3rd element of each entry are:
METH_VARARGS - Typical Case
    The function expects two PyObject* values. The first one is the self object for methods; for module functions, it has the value given to Py_InitModule4() (or NULL if Py_InitModule() was used). The second parameter (often called args) is a tuple object representing all arguments. This parameter is typically processed using PyArg_ParseTuple() or PyArg_UnpackTuple. 

METH_KEYWORDS - Define Functions with Keyword Arguments
    The function expects three parameters: self, args, and a dictionary of all the keyword arguments. The flag is typically combined with METH_VARARGS, and the parameters are typically processed using PyArg_ParseTupleAndKeywords(). 

METH_NOARGS - Optimized No Argument Case
    Methods without parameters don't need to check whether arguments are given if they are listed with the METH_NOARGS flag. When used with object methods, the first parameter is typically named self and will hold a reference to the object instance. In all cases the second parameter will be NULL. 

METH_O - Optimized Single Argument Case
    Methods with a single object argument can be listed with the METH_O flag, instead of invoking PyArg_ParseTuple() with a "O" argument. They have the type PyCFunction, with the self parameter, and a PyObject* parameter representing the single argument. 
 
*/

static PyMethodDef mpiMethods[] = {
    {"count_neighbors", count_neighbors, METH_VARARGS, "count_neighbors"},
    {NULL, NULL, 0, NULL}	/* Sentinel */
};

/* defines and initializes module "_mpi" */
void init_engine(void)
{
    PyObject *m;		/*, *d; */
    /*PyObject *tmp; */
    import_array();
    m = Py_InitModule3("_engine", mpiMethods, "_engine module");
    PyObject *mpiException = PyErr_NewException("mpi.Exception", NULL, NULL);
    Py_INCREF(mpiException);
    PyModule_AddObject(m, "mpiException", mpiException);
    return;
}

