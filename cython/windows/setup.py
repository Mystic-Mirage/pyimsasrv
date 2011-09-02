# Run as:
#    python setup.py build_ext --inplace

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

ext_modules = cythonize("asta.py")

setup(
  name = 'asta',
  ext_modules = ext_modules,
)
