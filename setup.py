# -*- coding: utf-8 -*-
from distutils.core import setup
import setuptools

setup(
    name='decorated',
    version='1.9.9',
    author='Mengchen LEE',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
    ],
    description='Decorator framework and common decorators for python.',
    extras_require={
        'test': [
            'fixtures>=3.0.0',
            'pylru>=1.0.9',
        ],
    },
    install_requires=[
        'fixtures2>=0.1.2',
        'six>=1.11.0',
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    url='https://github.com/cooledcoffee/decorated',
)
