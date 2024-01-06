#!/usr/bin/env python
# coding: utf-8
from setuptools import setup, find_packages

VERSION = '0.0.5'

setup(
    name='cc-feishu',  # package name
    version=VERSION,  # package version
    description='my feishu package',  # package description
    packages=find_packages(),
    url="https://github.com/houm01/cc-feishu",
    zip_safe=False,
)

