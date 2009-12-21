from distutils.core import setup, Extension

files = ["example.c","example.i"]

libraries = []
#libraries = ["efence"] # uncomment to use ElectricFence
includes = ['include', 'python']
setup(name = "example", version = "0.3",
       ext_modules = [Extension("_example", files,
                                libraries = libraries,
                                include_dirs =  includes,
                               )
                     ],
      )
