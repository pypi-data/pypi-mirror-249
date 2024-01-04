#!/usr/bin/env python
# coding: utf-8
from setuptools import setup

VERSION = '0.0.1'

setup(
    name='cc-feishu',  # package name
    version=VERSION,  # package version
    description='my feishu package',  # package description
    packages=['feishu_client'],
    url="https://github.com/houm01/cc-feishu",
    zip_safe=False,
)

