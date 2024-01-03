#!/usr/bin/env python
# coding: utf-8
from setuptools import setup
from setuptools import find_packages

VERSION = '0.0.2'

setup(
    name='cc_notion',  # package name
    version=VERSION,  # package version
    description='my package',  # package description
    packages=find_packages(),
    zip_safe=False,
)
