#include <Python.h>
#include <mpi.h>

static PyObject *
mpimodule_rank( PyObject *self, PyObject *args );
    
static PyMethodDef MpimoduleMethods[] = {
    {"rank", mpimodule_rank, METH_VARARGS,"Execute MPI_Comm_rank and return an integer rank value."},
     {NULL,NULL,0,NULL}
     };

static PyObject *MpimoduleError;

    PyMODINIT_FUNC
initmpimodule(void)
{
    PyObject *m; 
    m = Py_InitModule("mpimodule", MpimoduleMethods);

    MpimoduleError = PyErr_NewException("mpimodule.error",NULL,NULL);
    Py_INCREF(MpimoduleError);
    PyModule_AddObject(m, "error", MpimoduleError);
}

static PyObject *
mpimodule_rank( PyObject *self, PyObject *args )
{
    int flag;
    int rank;
    if( MPI_Initialized(&flag) ) // MPI not initialized
        return Py_BuildValue("i",-1);
    if( ! flag ) // Failure to call MPI_Initialized
        return Py_BuildValue("i",-2);
    else
        MPI_Comm_rank(MPI_COMM_WORLD,&rank);
        return Py_BuildValue("i",rank);
}


