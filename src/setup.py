# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='decorated',
    version='1.2.8',
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
    description='Base components for easily writing decorators.',
    install_requires=[
        'six',
    ],
    packages=[
        'decorated',
        'decorated.base',
        'decorated.decorators',
        'decorated.util',
    ],
    url='https://github.com/CooledCoffee/decorated/',
)
