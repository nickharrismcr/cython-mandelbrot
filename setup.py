from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

import numpy # to get includes
import os,re

# setup(
#      cmdclass = {'build_ext': build_ext},
#      ext_modules = cythonize(*pyx"),
#      include_dirs = [numpy.get_include(),],
#  )

 
extensions = [ 
        
    Extension( "mandel2" , ["mandel2.pyx"],
               include_dirs=[numpy.get_include(),],
               extra_compile_args=["/openmp",],
               extra_link_args=["/openmp",],
                ),
    Extension( "julia" , ["julia.pyx"],
               include_dirs=[numpy.get_include(),],
               extra_compile_args=["/openmp",],
               extra_link_args=["/openmp",],
                ),
             ]

setup(
      name="mandelbrot",
      ext_modules=cythonize(extensions),
        
)     


import main