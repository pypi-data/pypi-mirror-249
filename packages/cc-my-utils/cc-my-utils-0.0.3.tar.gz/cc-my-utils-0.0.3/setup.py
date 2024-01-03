#!/usr/bin/env python
# coding: utf-8
from setuptools import setup
from setuptools import find_packages

VERSION = '0.0.3'

setup(
    name='cc-my-utils',  # package name
    version=VERSION,  # package version
    description='my utils package',  # package description
    packages=find_packages(),
    url="https://github.com/houm01/cc-utils",
    zip_safe=False,
)

