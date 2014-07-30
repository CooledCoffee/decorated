# -*- coding: utf-8 -*-
from decorated.base.function import WrapperFunction
from fixtures2 import TestCase

class BeforeTest(TestCase):
    def test(self):
        # set up
        class TestFunction(WrapperFunction):
            def _before(self, *args, **kw):
                BeforeTest.args = self._resolve_args(*args, **kw)
        @TestFunction
        def foo(a, b=0):
            return 1
        
        # test
        result = foo(1, b=2)
        self.assertEqual(1, result)
        self.assertEqual({'a': 1, 'b': 2}, self.args)
        
class AfterTest(TestCase):
    def test_success(self):
        # set up
        class TestFunction(WrapperFunction):
            def _after(self, ret, error, *args, **kw):
                AfterTest.args = self._resolve_args(*args, **kw)
                AfterTest.ret = ret
                AfterTest.error = error
        @TestFunction
        def foo(a, b=0):
            return 1
        
        # test
        result = foo(1, b=2)
        self.assertEqual(1, result)
        self.assertEqual({'a': 1, 'b': 2}, self.args)
        self.assertEqual(1, self.ret)
        self.assertEqual(None, self.error)
        
    def test_error(self):
        # set up
        class TestFunction(WrapperFunction):
            def _after(self, ret, error, *args, **kw):
                AfterTest.args = self._resolve_args(*args, **kw)
                AfterTest.ret = ret
                AfterTest.error = error
        @TestFunction
        def foo(a, b=0):
            raise Exception()
        
        # test
        with self.assertRaises(Exception):
            foo(1, b=2)
        self.assertEqual({'a': 1, 'b': 2}, self.args)
        self.assertIsNone(self.ret)
        self.assertIsInstance(self.error, Exception)
        
    def test_success_but_error_in_after(self):
        # set up
        class TestFunction(WrapperFunction):
            def _after(self, ret, error, *args, **kw):
                AfterTest.ret = ret
                raise Exception()
        @TestFunction
        def foo(a, b=0):
            return 1
        
        # test
        with self.assertRaises(Exception):
            foo(1, b=2)
        self.assertEqual(1, self.ret)
        
    def test_error_and_error_in_after(self):
        # set up
        class TestFunction(WrapperFunction):
            def _after(self, ret, error, *args, **kw):
                raise Exception('after error')
        @TestFunction
        def foo(a, b=0):
            raise Exception('original error')
        
        # test
        with self.assertRaises(Exception) as ctx:
            foo(1, b=2)
        self.assertEqual('after error', str(ctx.exception))
        