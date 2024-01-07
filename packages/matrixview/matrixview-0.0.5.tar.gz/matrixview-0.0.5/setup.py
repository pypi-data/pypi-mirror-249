#!python
# -*- coding:utf-8 -*-
from __future__ import print_function
from setuptools import setup, find_packages
import matrixview

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="matrixview",
    version=matrixview.__version__,
    author="eeshikm",
    author_email="eeshikm@163.com",
    description="!⚆_⚆ This is a very powerful matrix element viewer !",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com",
    py_modules=['matrixview'],
    install_requires=[
        'keyboard'
    ],
    classifiers=[

        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ]
)

