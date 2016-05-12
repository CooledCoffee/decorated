# -*- coding: utf-8 -*-
from decorated.base.function import Function
import logging
import time

log = logging.getLogger(__name__)

class Retries(Function):
    def _init(self, times, delay=0, error_types=(Exception,)):
        if times < 0:
            raise Exception('Times cannot be negative.')
        self._times = times
        self._delay = delay
        self._error_types = error_types
        
    def _call(self, *args, **kw):
        times = 0
        while True:
            try:
                return super(Retries, self)._call(*args, **kw)
            except Exception as e:
                times += 1
                if times <= self._times and isinstance(e, self._error_types):
                    log.warn('Execution failed. Will retry in %f seconds.' % self._delay)
                    time.sleep(self._delay)
                else:
                    log.warn('Execution failed permanently.')
                    raise
        