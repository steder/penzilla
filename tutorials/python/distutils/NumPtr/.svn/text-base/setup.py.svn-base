import os, glob

# Gather up all the files we need.

files = glob.glob("*.c")
files += glob.glob("*.i") 
## pfiles = glob.glob("*.py")
## i = 0
## while i < len(pfiles):
##     pfiles[i] = os.path.splitext(pfiles[i])[0]
##     i += 1

## Distutils Script
#
from distutils.core import setup, Extension

# Some useful directories.  
from distutils.sysconfig import get_python_inc, get_python_lib

python_incdir = os.path.join( get_python_inc(plat_specific=1) )
python_libdir = os.path.join( get_python_lib(plat_specific=1) )

setup(name="NumPtr",
      version="1.0a",
      description="CliMT - CSC Climate Modeling Toolkit",
      author="Rodrigo Caballero",
      author_email="rca@geosci.uchicago.edu",
      url="http://geosci.uchicago.edu/~rca/climt.tar",
      ext_modules = [Extension('_NumPtr',
                               files,
                               include_dirs=[python_incdir],
                               library_dirs=[python_libdir],
                               ),
                     ],
      # Install these to their own directory
      #   *I want to be able to remove them if I screw up this script
      #   *"Sandboxing", if you will
      extra_path = 'NumPtr',
      py_modules=["NumPtr","test"],
     )
