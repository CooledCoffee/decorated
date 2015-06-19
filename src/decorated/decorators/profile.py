# -*- coding: utf-8 -*-
from cProfile import Profile as RawProfile
from decorated.base.function import Function
from decorated.util import reporters
from decorated.util.gcutil import DisableGc
from pstats import Stats
from six import StringIO
import doctest

class Profile(Function):
    def _call(self, *args, **kw):
        profile = RawProfile()
        def _run():
            with DisableGc():
                for _ in range(self._iterations):
                    _run.result = super(Profile, self)._call(*args, **kw)
        profile.runctx('_run()', {}, {'_run': _run})
        profile.create_stats()
        stats = Stats(profile)
        stats.sort_stats('cumulative')
        stats.fcn_list = stats.fcn_list[:self._max_lines]
        self._reporter(stats)
        return _run.result
    
    def _init(self, iterations=1, reporter=reporters.PRINT_REPORTER, max_lines=50):
        super(Profile, self)._init()
        self._iterations = iterations
        self._reporter = reporter
        self._max_lines = max_lines
        
class Stats(Stats):
    def __str__(self):
        '''
        >>> result = str(Stats(RawProfile().run('')))
        >>> 'function calls' in result
        True
        '''
        self.stream = StringIO()
        self.print_stats()
        return self.stream.getvalue()
    
if __name__ == '__main__':
    doctest.testmod()
    