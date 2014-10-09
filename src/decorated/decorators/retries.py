# -*- coding: utf-8 -*-
from decorated.base.function import Function
import time

ENABLED = True

class Retries(Function):
    def _init(self, times, delay=0):
        if times <= 0:
            raise Exception('Times should be positive.')
        self._times = times
        self._delay = delay
        
    def _call(self, *args, **kw):
        if not ENABLED:
            return super(Retries, self)._call(*args, **kw)
        
        for i in range(self._times):
            try:
                return super(Retries, self)._call(*args, **kw)
            except Exception as e:
                last_error = e
                if i < self._times - 1:
                    time.sleep(self._delay)
        else:
            raise last_error
        