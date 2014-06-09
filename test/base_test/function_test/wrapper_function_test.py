# -*- coding: utf-8 -*-
from decorated.base.function import WrapperFunction
from fixtures2 import TestCase

class CallTest(TestCase):
    def test_before(self):
        # set up
        class TestFunction(WrapperFunction):
            def _before(self, *args, **kw):
                CallTest.args = self._resolve_args(*args, **kw)
        @TestFunction
        def foo(a, b=0):
            return 1
        
        # test
        result = foo(1, b=2)
        self.assertEqual(1, result)
        self.assertEqual({'a': 1, 'b': 2}, self.args)
        
    def test_after_success(self):
        # set up
        class TestFunction(WrapperFunction):
            def _after(self, ret, error, *args, **kw):
                CallTest.args = self._resolve_args(*args, **kw)
                CallTest.ret = ret
                CallTest.error = error
        @TestFunction
        def foo(a, b=0):
            return 1
        
        # test
        result = foo(1, b=2)
        self.assertEqual(1, result)
        self.assertEqual({'a': 1, 'b': 2}, self.args)
        self.assertEqual(1, self.ret)
        self.assertEqual(None, self.error)
        
    def test_after_error(self):
        # set up
        class TestFunction(WrapperFunction):
            def _after(self, ret, error, *args, **kw):
                CallTest.args = self._resolve_args(*args, **kw)
                CallTest.ret = ret
                CallTest.error = error
        @TestFunction
        def foo(a, b=0):
            raise Exception()
        
        # test
        with self.assertRaises(Exception):
            foo(1, b=2)
        self.assertEqual({'a': 1, 'b': 2}, self.args)
        self.assertIsNone(self.ret)
        self.assertIsInstance(self.error, Exception)
        