%module NumPtr

%{
#include "Python.h"
#include "Numeric/arrayobject.h"
%}

int   getstride1(PyObject *array);

double *   getpointer1(PyObject *array);
double **  getpointer2(PyObject *array);
double *** getpointer3(PyObject *array);

void  test1(double *   a, int n);
void  test2(double **  a, int n, int m);
void  test3(double *** a, int n, int m, int l);
