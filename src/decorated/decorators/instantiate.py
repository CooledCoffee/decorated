# -*- coding: utf-8 -*-
from decorated.base.function import Function

class Instantiate(Function):
    def _decorate(self, cls):
        self.class_ = cls
        def _func(*args, **kw):
            obj = cls()
            method = getattr(obj, self._method)
            return method(*args, **kw)
        _func.__name__ = cls.__name__
        _func.__module__ = cls.__module__
        _func.__doc__ = cls.__doc__
        return super(Instantiate, self)._decorate(_func)
    
    def _init(self, method='__call__'):
        super(Instantiate, self)._init()
        self._method = method
        