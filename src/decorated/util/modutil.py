# -*- coding: utf-8 -*-
import doctest
import importlib
import pkgutil
import sys

def load_tree(root):
    mod_or_pack = importlib.import_module(root)
    if hasattr(mod_or_pack, '__path__'):
        for _, mod, _ in pkgutil.walk_packages(path=mod_or_pack.__path__, prefix=mod_or_pack.__name__ + '.'):
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
    