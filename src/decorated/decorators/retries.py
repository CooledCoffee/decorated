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
        times = 0
        while True:
            try:
                return super(Retries, self)._call(*args, **kw)
            except Exception:
                times += 1
                if times <= self._times:
                    time.sleep(self._delay)
                else:
                    raise
        
