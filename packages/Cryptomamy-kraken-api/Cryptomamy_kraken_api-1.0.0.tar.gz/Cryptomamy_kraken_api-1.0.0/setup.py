#!/usr/bin/env python3

import os.path
from distutils.core import setup

# Importing the version from the kraken_api package
exec(open('Cryptomamy_kraken_api/version.py').read())

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


# Ensure there are two blank lines before the setup function
setup(
    name='Cryptomamy_kraken_api',
    version=__version__,
    description='kraken.com cryptocurrency exchange API',
    long_description=read('README.rst'),
    long_description_content_type='text/x-rst',
    author='Cryptomamy',
    author_email='cryptomamy@protonmail.com',
    url=__url__,
    install_requires=[
        'requests>=2.18.2,<3'
    ],
    packages=['Cryptomamy_kraken_api'],
    python_requires='>=3.3',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
