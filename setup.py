#!/usr/bin/env python

from setuptools import setup

with open('VERSION', 'r') as f:
    version = f.read()

setup(name='corgi',
      version=version,
      description='Python data and analysis tools',
      author='Paul English',
      author_email='paulnglsh@gmail.com',
      url='https://github.com/log0ymxm/corgi',
      packages=['corgi'],
      install_requires=[
          'numpy',
          'six',
          'sqlalchemy',
      ],
      )
