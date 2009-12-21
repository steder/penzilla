#include <stdio.h>
#include <stdlib.h>

double ave( int n, double *array );

double ave( int n, double *array )
{
  int i;
  double sum;
  for( i = 0; i < n; i++ )
  {
    sum += array[i];
  } 
  return (double)( sum / n );
}
