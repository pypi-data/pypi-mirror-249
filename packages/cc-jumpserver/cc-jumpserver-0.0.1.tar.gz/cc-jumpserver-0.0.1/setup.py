#!/usr/bin/env python
# coding: utf-8
from setuptools import setup
from setuptools import find_packages

VERSION = '0.0.1'

setup(
    name='cc-jumpserver',  # package name
    version=VERSION,  # package version
    description='jumpserver sdk',  # package description
    packages=find_packages(),
    url="https://github.com/houm01/cc-jumpserver",
    zip_safe=False,
)

