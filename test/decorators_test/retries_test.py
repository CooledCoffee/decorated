# -*- coding: utf-8 -*-
from fixtures2 import TestCase

from decorated.decorators.retries import Retries


class RetriesTest(TestCase):
    def test_success_at_first(self):
        @Retries(3)
        def foo():
            return 1
        result = foo()
        self.assertEqual(1, result)
        
    def test_success_after_retry(self):
        @Retries(3)
        def foo():
            foo.times += 1
            if foo.times == 3:
                return 1
            else:
                raise Exception('Failed at retry %d.' % foo.times)
        foo.times = 0
        result = foo()
        self.assertEqual(1, result)
        
    def test_all_failed(self):
        @Retries(3)
        def foo():
            foo.times += 1
            raise Exception()
        foo.times = 0
        with self.assertRaises(Exception):
            foo()
        self.assertEqual(4, foo.times)
        
    def test_error_types(self):
        @Retries(3, error_types=(IOError, TypeError))
        def foo():
            foo.times += 1
            raise Exception()
        foo.times = 0
        with self.assertRaises(Exception):
            foo()
        self.assertEqual(1, foo.times)
