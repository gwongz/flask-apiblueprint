"""
Flask-APIBlueprint
-------------

Route inheritance for Flask Blueprints.

"""
from setuptools import setup

try:
    with open('LONG_DESCRIPTION.rst') as f:
        long_description = f.read()
except:
    long_description = 'Route inheritance for Flask Blueprints'


setup(
    name='Flask-APIBlueprint',
    version='0.1',
    url='https://github.com/gwongz/flask-apiblueprint',
    license='BSD',
    author='Grace Wong',
    author_email='gwongz@gmail.com',
    description='Route inheritance for Flask Blueprints',
    long_description=long_description,
    packages=['flask_apiblueprint'],
    zip_safe=False,
    include_package_data=True,
    download_url='https://github.com/gwongz/flask-apiblueprint/tarball/0.1',
    platforms='any',
    install_requires=[
        'Flask'
    ],
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
        'Programming Language :: Python :: 2.7'
    ]
)