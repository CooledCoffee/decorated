# -*- coding: utf-8 -*-
from decorated.base.function import Function
import time

class Retries(Function):
    def _init(self, times, delay=0):
        if times < 0:
            raise Exception('Times cannot be negative.')
        self._times = times
        self._delay = delay
        
    def _call(self, *args, **kw):
        for i in range(self._times + 1):
            try:
                return super(Retries, self)._call(*args, **kw)
            except Exception as e:
                last_error = e
                if i < self._times - 1:
                    time.sleep(self._delay)
        else:
            raise last_error
        