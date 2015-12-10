#!/usr/bin/env python

from setuptools import setup

with open('VERSION', 'r') as f:
    version = f.read()

setup(name='use',
      version=version,
      description='Python data and analysis tools',
      author='Paul English',
      author_email='paulnglsh@gmail.com',
      url='https://github.com/log0ymxm/use',
      packages=['use'],
      install_requires=[
          'numpy',
          'six',
          'sqlalchemy',
      ],
      )
