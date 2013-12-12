# -*- coding: utf-8 -*-
import importlib
import inspect
import pkgutil

def load_modules(packages):
    if not isinstance(packages, (list, tuple)):
        packages = [packages]
    pathes = []
    for p in packages:
        if not inspect.ismodule(p):
            p = importlib.import_module(p)
        pathes.extend(p.__path__)
    for loader, mod, _ in pkgutil.walk_packages(pathes):
        loader.find_module(mod).load_module(mod)
        