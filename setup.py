#!/usr/bin/env python3

import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='amocrm',
    version='0.7.1',
    packages=['amocrm'],
    install_requires=['requests'],
    include_package_data=True,
    license='BSD License',  
    description='AmoCRM API wrapper in python',
    long_description=README,
    url='https://github.com/paramono/amocrm',
    author='Alexander Paramonov',
    author_email='alex@paramono.com',
    classifiers=[
        'Environment :: Console',
        'Environment :: Plugins',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Office/Business',
        'Topic :: Office/Business :: Financial',
    ],
)
