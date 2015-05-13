# -*- coding: utf-8 -*-
from decorated.base.function import Function
from decorated.util import reporters
from decorated.util.gcutil import DisableGc
import doctest
import sys
import time

if sys.platform == "win32":
    # On Windows, the best timer is time.clock()
    timer = time.clock
else:
    # On most other platforms the best timer is time.time()
    timer = time.time

class TimeIt(Function):
    def _call(self, *args, **kw):
        timings = [None] * self._repeats
        with DisableGc():
            for i in range(self._repeats):
                begin = timer()
                for _ in range(self._iterations):
                    result = super(TimeIt, self)._call(*args, **kw)
                seconds = timer() - begin
                timings[i] = seconds
        timing = Result(self._func, args, kw, self._iterations,
                self._repeats, timings)
        self._reporter(timing)
        return result
    
    def _init(self, iterations=1, repeats=1, reporter=reporters.PRINT_REPORTER):
        super(TimeIt, self)._init()
        self._iterations = iterations
        self._repeats = repeats
        self._reporter = reporter
        
class Result(object):
    def __init__(self, func, args, kwargs, iterations, repeats, timings):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.iterations = iterations
        self.repeats = repeats
        self.timings = timings
        
    def __str__(self):
        '''
        basic
        >>> def foo(): pass
        >>> foo.__module__ = 'aaa.bbb'
        >>> str(Result(foo, [], {}, 10, 3, [0.05, 0.1, 0.15]))
        'Timing of aaa.bbb.foo(): [0.05, 0.1, 0.15] (iterations=10)'
        
        with args
        >>> def foo(a): pass
        >>> foo.__module__ = 'aaa.bbb'
        >>> str(Result(foo, [1], {}, 10, 3, [0.05, 0.1, 0.15]))
        'Timing of aaa.bbb.foo(1): [0.05, 0.1, 0.15] (iterations=10)'
        
        with kwargs
        >>> def foo(a, b=0): pass
        >>> foo.__module__ = 'aaa.bbb'
        >>> str(Result(foo, [1], {'b': 2}, 10, 3, [0.05, 0.1, 0.15]))
        'Timing of aaa.bbb.foo(1, b=2): [0.05, 0.1, 0.15] (iterations=10)'
        '''
        kwargs = ['%s=%s' % (k, v) for k, v in self.kwargs.items()]
        args = [str(arg) for arg in self.args] + kwargs
        args = ', '.join(args)
        return 'Timing of %s.%s(%s): %s (iterations=%d)' \
                % (self.func.__module__, self.func.__name__, args, self.timings, self.iterations)
    
if __name__ == '__main__':
    doctest.testmod()
    