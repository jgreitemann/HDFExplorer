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
      data_files=[('share/applications', ['h5explorer.desktop']),
                  ('share/icons/hicolor/256x256/mimetypes', ['icons/hicolor/256x256/mimetypes/application-x-hdf.png']),
                  ('share/icons/hicolor/48x48/mimetypes', ['icons/hicolor/48x48/mimetypes/application-x-hdf.png']),
                  ('share/icons/hicolor/32x32/mimetypes', ['icons/hicolor/32x32/mimetypes/application-x-hdf.png']),
                  ('share/icons/hicolor/24x24/mimetypes', ['icons/hicolor/24x24/mimetypes/application-x-hdf.png']),
                  ('share/icons/hicolor/16x16/mimetypes', ['icons/hicolor/16x16/mimetypes/application-x-hdf.png'])]
     )
