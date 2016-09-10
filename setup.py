#!/usr/bin/env python3

from distutils.core import setup

setup(name='HDFExplorer',
      version='0.1',
      description='Graphically browse HDF5 files',
      author='Jonas Greitemann',
      author_email='jgreitemann@gmail.com',
      url='https://www.github.com/jgreitemann/HDFExplorer',
      packages=['hdfexplorer'],
      package_dir={'hdfexplorer': 'hdfexplorer'},
      scripts=['h5explorer'],
      package_data={'hdfexplorer': ['data/icons/dataset.png']},
      data_files=[('share/applications', ['h5explorer.desktop']),
                  ('share/icons/hicolor/256x256/apps', ['data/icons/256x256/apps/jgreitemann-h5explorer.png']),
                  ('share/icons/hicolor/48x48/apps', ['data/icons/48x48/apps/jgreitemann-h5explorer.png']),
                  ('share/icons/hicolor/16x16/apps', ['data/icons/16x16/apps/jgreitemann-h5explorer.png']),
                  ('share/icons/hicolor/256x256/mimetypes', ['data/icons/256x256/mimetypes/application-x-hdf.png']),
                  ('share/icons/hicolor/48x48/mimetypes', ['data/icons/48x48/mimetypes/application-x-hdf.png']),
                  ('share/icons/hicolor/32x32/mimetypes', ['data/icons/32x32/mimetypes/application-x-hdf.png']),
                  ('share/icons/hicolor/24x24/mimetypes', ['data/icons/24x24/mimetypes/application-x-hdf.png']),
                  ('share/icons/hicolor/16x16/mimetypes', ['data/icons/16x16/mimetypes/application-x-hdf.png'])]
     )
