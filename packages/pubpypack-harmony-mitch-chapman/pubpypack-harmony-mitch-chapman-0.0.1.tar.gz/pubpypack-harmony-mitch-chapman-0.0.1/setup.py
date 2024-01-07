from setuptools import setup, Extension
from Cython.Build import cythonize

# Need this in order to convince Cython that the build artifact belongs in
# imppkg, not in src/imppkg.  Submit as change suggestion?
# Python 3.11.6; setuptools 68.2.2; Cython 3.0.6
extension = Extension("imppkg.harmonic_mean", ["src/imppkg/harmonic_mean.pyx"])
ext_module = cythonize(extension)
setup(ext_modules=ext_module)
