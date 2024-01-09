#  -*- coding: utf-8 -*-
"""

Author: Rafael R. L. Benevides
Date: 1/26/23

"""

from setuptools import Extension, setup  # must be on top

import numpy
from Cython.Build import cythonize


# ========== ========== ========== ========== ========== ========== ext_modules
cython_compiler_directives = {
    'language_level': '3',
    'embedsignature': True,
    'cdivision': True,
    'boundscheck': False,
    'wraparound': False,
    'profile': True
}
"""Refer to
https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#compiler-directives
"""

options = {
    'include_dirs': [numpy.get_include()],
    'define_macros': [("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]
}

extensions = [
    Extension('aftk.mathtools.psdm', ['aftk/mathtools/psdm.pyx'], **options),
    Extension('aftk.mathtools.spharm', ['aftk/mathtools/spharm.pyx'], **options),
    Extension('aftk.mathtools.sphankel', ['aftk/mathtools/sphankel.pyx'], **options),
]

ext_modules = cythonize(extensions,
                        annotate=True,
                        compiler_directives=cython_compiler_directives,
                        include_path=[numpy.get_include()])

# ========== ========== ========== ========== ========== ========== package data
package_data = {
    'aftk': ['*.pyx', '*.pxd'],
    'aftk.mathtools': ['*.pyx', '*.pxd']
}


# ========== ========== ========== ========== ========== ========== setup
setup(ext_modules=ext_modules,
      include_package_data=True,
      package_data=package_data)
