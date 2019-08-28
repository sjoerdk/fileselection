#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['pyyaml']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Sjoerd Kerkstra",
    author_email='w.s.kerkstra@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
    description="Persistable lists of selected_paths",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='fileselection',
    name='fileselection',
    packages=find_packages(include=['fileselection']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/sjoerdk/fileselection',
    version='0.1.7',
    zip_safe=False,
)
