# -*- coding: utf-8 -*-
import doctest
import importlib
import inspect
import pkgutil
import sys

def load_modules(packages):
    if not isinstance(packages, (list, tuple)):
        packages = [packages]
    for package in packages:
        if not inspect.ismodule(package):
            package = importlib.import_module(package)
        for _, mod, _ in pkgutil.walk_packages(path=package.__path__, prefix=package.__name__ + '.'):
            if mod not in sys.modules:
                importlib.import_module(mod)
                
def module_exists(modname):
    '''
    >>> module_exists('decorated.util.modutil')
    True
    >>> module_exists('fakepackage.fakemod')
    False
    '''
    try:
        importlib.import_module(modname)
        return True
    except ImportError:
        return False
    
if __name__ == '__main__':
    doctest.testmod()
    