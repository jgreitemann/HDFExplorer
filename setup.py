#!/usr/bin/env python3

from distutils.core import setup

setup(name='HDFExplorer',
      version='0.1',
      description='Graphically browse HDF5 files',
      author='Jonas Greitemann',
      author_email='jgreitemann@gmail.com',
      url='https://www.github.com/jgreitemann/HDFExplorer',
      packages=['hdfexplorer'],
      scripts=['h5explorer'],
     )
