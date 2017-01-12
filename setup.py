#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Flask-APIBlueprint
-------------

Route inheritance for Flask Blueprints.

"""
try:
    from setuptools import setup, find_packages
except ImportError:
    from disutils.core import setup

try:
    with open('LONG_DESCRIPTION.rst') as f:
        long_description = f.read()
except:
    long_description = 'Route inheritance for Flask Blueprints'

requirements = [
    "flask>=0.11.1, <1.0",
    "six>=1.10.0, <2.0"
]

setup(
    name='Flask-APIBlueprint',
    version='1.0.0',
    url='https://github.com/gwongz/flask-apiblueprint',
    license='BSD',
    author='Grace Wong',
    author_email='gwongz@gmail.com',
    description='Route inheritance for Flask Blueprints',
    long_description=long_description,
    packages=['flask_apiblueprint'],
    zip_safe=False,
    include_package_data=True,
    download_url='https://github.com/gwongz/flask-apiblueprint/tarball/v1.0.0',
    platforms='any',
    install_requires=requirements,
    test_suite='test_apiblueprint',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3'
    ]
)
