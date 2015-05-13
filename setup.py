# -*- coding: utf-8 -*-
from distutils.core import setup
import setuptools

setup(
    name='decorated',
    version='1.6',
    author='Mengchen LEE',
    author_email='CooledCoffee@gmail.com',
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
    install_requires=[
        'fixtures2>=0.1.2',
        'six',
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    url='https://github.com/CooledCoffee/decorated/',
)
