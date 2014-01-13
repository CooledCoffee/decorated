# -*- coding: utf-8 -*-
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
        for loader, mod, _ in pkgutil.walk_packages(path=package.__path__, prefix=package.__name__ + '.'):
            if mod not in sys.modules:
                loader.find_module(mod).load_module(mod)
                