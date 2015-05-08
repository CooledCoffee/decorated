# -*- coding: utf-8 -*-
from decorated.decorators.profile import Profile, Stats
from fixtures2 import TestCase

stats = None
def _reporter(s):
    global stats
    stats = s

class ProfileTest(TestCase):
    def test_basic(self):
        # set up
        @Profile(reporter=_reporter)
        def foo(a, b=0):
            foo.times += 1
            return 1
        foo.times = 0
        
        # test
        result = foo(1)
        self.assertEqual(1, result)
        self.assertEqual(1, foo.times)
        self.assertIsInstance(stats, Stats)

    def test_iterations(self):
        # set up
        @Profile(iterations=10, reporter=_reporter)
        def foo(a, b=0):
            foo.times += 1
            return 1
        foo.times = 0
        
        # test
        result = foo(1)
        self.assertEqual(1, result)
        self.assertEqual(10, foo.times)
        self.assertIsInstance(stats, Stats)
        