#!/usr/bin/env python

from setuptools import setup

setup(name='Distutils',
      version='1.0',
      description='CLI front-end to retargeting features of radiotool',
      author='Ronen Barzel',
      author_email='ronen@barzel.org',
      url='https://github.com/ronen/retarget-py',
      packages=[],
      install_requires=["radiotool", "path.py"],
      scripts=["retarget.py"]
     )
