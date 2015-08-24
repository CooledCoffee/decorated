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
            def _after(self, ret, *args, **kw):
                AfterTest.args = self._resolve_args(*args, **kw)
                AfterTest.ret = ret
        @TestFunction
        def foo(a, b=0):
            return 1
        
        # test
        result = foo(1, b=2)
        self.assertEqual(1, result)
        self.assertEqual({'a': 1, 'b': 2}, self.args)
        self.assertEqual(1, self.ret)
        
    def test_error(self):
        # set up
        AfterTest.called = False
        class TestFunction(WrapperFunction):
            def _after(self, ret, error, *args, **kw):
                AfterTest.called = True
        @TestFunction
        def foo(a, b=0):
            raise Exception()
        
        # test
        with self.assertRaises(Exception):
            foo(1, b=2)
        self.assertFalse(self.called)
        
class ErrorTest(TestCase):
    def test_success(self):
        # set up
        ErrorTest.called = False
        class TestFunction(WrapperFunction):
            def _error(self, err, *args, **kw):
                AfterTest.called = True
        @TestFunction
        def foo(a, b=0):
            return 1
        
        # test
        result = foo(1, b=2)
        self.assertEqual(1, result)
        self.assertFalse(self.called)
        
    def test_error(self):
        # set up
        class TestFunction(WrapperFunction):
            def _error(self, err, *args, **kw):
                ErrorTest.err = err
                ErrorTest.args = self._resolve_args(*args, **kw)
        @TestFunction
        def foo(a, b=0):
            raise Exception()
        
        # test
        with self.assertRaises(Exception):
            foo(1, b=2)
        self.assertIsInstance(self.err, Exception)
        self.assertEqual({'a': 1, 'b': 2}, self.args)
        