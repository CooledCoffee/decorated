# -*- coding: utf-8 -*-
from decorated.util import retries
from unittest.case import TestCase

class RetriesTest(TestCase):
    def test_success_at_first(self):
        @retries(3)
        def foo():
            return 1
        result = foo()
        self.assertEqual(1, result)
        
    def test_success_after_retry(self):
        @retries(3)
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
        @retries(3)
        def foo():
            foo.times += 1
            raise Exception('Failed at retry %d.' % foo.times)
        foo.times = 0
        with self.assertRaises(Exception) as err:
            foo()
        self.assertEqual('Failed at retry 3.', str(err.exception))
        