# -*- coding: utf-8 -*-
from decorated.function import Function

class retries(Function):
    def _init(self, times):
        self._times = times
        
    def _call(self, *args, **kw):
        for _ in range(self._times):
            try:
                return super(retries, self)._call(*args, **kw)
            except Exception as e:
                last_error = e
        else:
            raise last_error
        