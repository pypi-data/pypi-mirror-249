#!/usr/bin/env python
# coding:utf-8
import os
import sys
import ctypes
import tempfile
from setuptools import find_packages, setup
from setuptools.command.install import install



setup(
    name='rbpop',
    version='0.1.1',
    description='(PyQt5 based) Pop your window at the right-bottom at the screen.',
    author_email='2229066748@qq.com',
    maintainer="Eagle'sBaby",
    maintainer_email='2229066748@qq.com',
    packages=find_packages(),
    license='Apache Licence 2.0',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows',
    ],
    keywords=['pyqt5', 'pop window'],
    python_requires='>=3',
    install_requires=[
        "PyQt5",
    ],
)
