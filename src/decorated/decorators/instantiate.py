# -*- coding: utf-8 -*-
from decorated.base.function import Function

class Instantiate(Function):
    def _decorate(self, cls):
        def _func(*args, **kw):
            obj = cls()
            method = getattr(obj, self._method)
            return method(*args, **kw)
        return super(Instantiate, self)._decorate(_func)
    
    def _init(self, method='__call__'):
        super(Instantiate, self)._init()
        self._method = method
        