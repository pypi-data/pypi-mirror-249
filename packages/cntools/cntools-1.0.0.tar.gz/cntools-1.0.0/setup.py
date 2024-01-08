from setuptools import setup, Extension
from Cython.Build import cythonize

setup(
    ext_modules=cythonize([Extension('_k_means_lloyd_reg', ['cntools/utils/_k_means_lloyd_reg.pyx'])])
)