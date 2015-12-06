#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='sympy_recursive',
      version='0.1.1',
      description='Resolve recursive sequences to explicit nth item formulas with SymPy.',
      url='http://github.com/hejmsdz/sympy_recursive',
      author='Mikołaj Rozwadowski',
      author_email='mikolaj.rozwadowski@outlook.com',
      license='MIT',
      packages=['sympy_recursive'],
      install_requires=[
          'sympy',
      ],
      zip_safe=False)
