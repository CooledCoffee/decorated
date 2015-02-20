# -*- coding: utf-8 -*-
from decorated.decorators.ignore_error import IgnoreError
from fixtures2 import TestCase

class CallTest(TestCase):
    def test_success(self):
        @IgnoreError
        def foo():
            return 1
        result = foo()
        self.assertEqual(1, result)
        
    def test_error(self):
        @IgnoreError
        def foo():
            raise Exception()
        result = foo()
        self.assertIsNone(result)
        