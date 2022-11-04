#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import exists

from setuptools import setup, find_packages

author = 'Donald Duck'
name = 'mypackage'
year = '2022'
version = '0.0.1'

setup(
    name=name,
    author=author,
    version=version,
    packages=find_packages(),
    package_dir={name: name},
    include_package_data=True,
    license='MIT',
    long_description=open('README.md').read() if exists('README.md') else '',
    long_description_content_type="text/markdown",
    install_requires=[],
    python_requires=">=3.6",
    classifiers=['Operating System :: OS Independent',
                 'Programming Language :: Python :: 3',
                 ],
    platforms=['ALL'],
)
