#!/usr/bin/env python
# coding: utf-8
from setuptools import setup
from setuptools import find_packages

VERSION = '0.0.1'

setup(
    name='cc-telegram',  # package name
    version=VERSION,  # package version
    description='my utils package',  # package description
    packages=find_packages(),
    url="https://github.com/houm01/cc-telegram",
    zip_safe=False,
)

