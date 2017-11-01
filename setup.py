#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import fetchman

extras_require_all = [
    'redis>=2.10.5',
    'requests>=2.13.0',
    'six>=1.10.0',
    'grequests>=0.3.0',
    'selenium>=2.53.6',
    'lxml>=3.7.2',
    'beautifulsoup4>=4.6.0',
]

setup(
        name='fetchman',
        version=fetchman.__version__,
        description=(
            'a simple spider system'
        ),
        author='DaVinciDW',
        author_email='darkwings_love@163.com',
        maintainer='DaVinciDW',
        maintainer_email='darkwings_love@163.com',
        license='Apache License, Version 2.0',
        packages=find_packages(exclude=['tests*']),
        platforms=["all"],
        url='https://github.com/DarkSand/fetchman',
        install_requires=extras_require_all,
        extras_require={
            'all': extras_require_all,
            'test': [
                'unittest2>=0.5.1',
                'coverage',
            ]
        },
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            "Environment :: Web Environment",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Topic :: Text Processing :: Indexing",
            "Topic :: Utilities",
            "Topic :: Internet",
            "Topic :: Software Development :: Libraries :: Python Modules",
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.4',
        ],
        test_suite='tests.all_suite',
)
