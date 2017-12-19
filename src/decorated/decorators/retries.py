# -*- coding: utf-8 -*-
import logging
import sys
import time

import six

from decorated.base.function import Function

log = logging.getLogger(__name__)

class Retries(Function):
    def _init(self, times, delay=0, error_types=(Exception,)): # pylint: disable=arguments-differ
        if times < 0:
            raise Exception('Times cannot be negative.')
        self._times = times
        self._delay = delay
        self._error_types = error_types
        
    def _call(self, *args, **kw):
        for i in six.moves.xrange(self._times + 1):
            try:
                return super(Retries, self)._call(*args, **kw)
            except Exception as e:
                if i < self._times and isinstance(e, self._error_types):
                    log.warn('Execution failed. Will retry in %f seconds.', self._delay, exc_info=True)
                    time.sleep(self._delay)
                else:
                    raise

class RetriesForever(Retries):
    def _init(self, delay=0, error_types=(Exception,)):
        super(RetriesForever, self)._init(sys.maxint - 1, delay=delay, error_types=error_types)
