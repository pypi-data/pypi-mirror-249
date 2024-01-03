#!/usr/bin/env python
# coding: utf-8
from setuptools import setup
from setuptools import find_packages

VERSION = '0.0.3'

setup(
    name='cc-notion',  # package name
    version=VERSION,  # package version
    description='my notion package',  # package description
    packages=find_packages(),
    zip_safe=False,
)

