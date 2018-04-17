# -*- coding: utf-8 -*-
import itertools
import logging
import time

import six

from decorated.base.function import Function

log = logging.getLogger(__name__)

class Retries(Function):
    def _init(self, times, delay=0, error_types=(Exception,)):
        self._times = times
        self._delay = delay
        self._error_types = error_types
        
    def _call(self, *args, **kw):
        for i in _iter(self._times):
            try:
                return super(Retries, self)._call(*args, **kw)
            except Exception as e:
                if i > 0 and isinstance(e, self._error_types):
                    log.warn('Execution failed. Will retry in %f seconds.', self._delay, exc_info=True)
                    time.sleep(self._delay)
                else:
                    raise

class RetriesForever(Retries):
    def _init(self, delay=0, error_types=(Exception,)):
        # noinspection PyTypeChecker
        super(RetriesForever, self)._init(None, delay=delay, error_types=error_types)


def _iter(times):
    '''
    >>> list(_iter(3))
    [3, 2, 1, 0]
    
    >>> it = _iter(None)
    >>> next(it)
    1
    >>> next(it)
    1
    '''
    if times is None:
        return itertools.cycle([1])
    else:
        # noinspection PyUnresolvedReferences
        return six.moves.xrange(times, -1, -1)
