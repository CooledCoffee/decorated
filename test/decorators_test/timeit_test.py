# -*- coding: utf-8 -*-
from decorated.decorators.timeit import TimeIt
from fixtures2 import TestCase

timing = None
def _reporter(r):
    global timing
    timing = r
    
class TimeItTest(TestCase):
    def test_basic(self):
        # set up
        @TimeIt(reporter=_reporter)
        def foo(a, b=0):
            return 1
        
        # test
        result = foo(1)
        self.assertEqual(1, result)
        self.assertEqual(1, timing.iterations)
        self.assertEqual(1, timing.repeats)
        self.assertEqual(1, len(timing.timings))
        
    def test_iterations(self):
        # set up
        @TimeIt(iterations=10, reporter=_reporter)
        def foo(a, b=0):
            foo.times += 1
            return 1
        foo.times = 0
        
        # test
        result = foo(1)
        self.assertEqual(1, result)
        self.assertEqual(10, foo.times)
        self.assertEqual(10, timing.iterations)
        self.assertEqual(1, timing.repeats)
        self.assertEqual(1, len(timing.timings))
        
    def test_repeats(self):
        # set up
        @TimeIt(repeats=10, reporter=_reporter)
        def foo(a, b=0):
            foo.times += 1
            return 1
        foo.times = 0
        
        # test
        result = foo(1)
        self.assertEqual(1, result)
        self.assertEqual(10, foo.times)
        self.assertEqual(1, timing.iterations)
        self.assertEqual(10, timing.repeats)
        self.assertEqual(10, len(timing.timings))
        
    def test_iterations_and_repeats(self):
        # set up
        @TimeIt(iterations=10, repeats=10, reporter=_reporter)
        def foo(a, b=0):
            foo.times += 1
            return 1
        foo.times = 0
        
        # test
        result = foo(1)
        self.assertEqual(1, result)
        self.assertEqual(100, foo.times)
        self.assertEqual(10, timing.iterations)
        self.assertEqual(10, timing.repeats)
        self.assertEqual(10, len(timing.timings))
        