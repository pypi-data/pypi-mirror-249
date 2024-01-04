#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Utilities for PyPI and twine"""
from __future__ import with_statement

import re

from setuptools import setup

# detect the current version
with open("glicko2.py", encoding="utf-8") as f:
    version = re.search(r"__version__\s*=\s*\'(.+?)\'", f.read()).group(  # type: ignore
        1
    )
if not version:
    raise ValueError("Version not found")


setup(
    name="glicko2",
    version=version,
    license="BSD",
    author="Heungsub Lee",
    author_email="s" r"u" r"b" r"@" r"s" r"u" r"b" r"l" r"." r"e" r"e",
    url="https://github.com/sublee/glicko2",
    description="The Glicko-2 rating system",
    long_description=__doc__,
    platforms="any",
    py_modules=["glicko2"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: Jython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Games/Entertainment",
    ],
    install_requires=["distribute"],
    test_suite="glicko2tests",
    tests_require=["pytest"],
)
