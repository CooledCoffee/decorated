# -*- coding: utf-8 -*-
from decorated.base.function import ContextFunction
from fixtures2 import TestCase

class CallTest(TestCase):
    def test_success(self):
        # set up
        class TestFunction(ContextFunction):
            def _before(self):
                CallTest.before_called = True
            def _after(self, ret):
                CallTest.after_called = True
                CallTest.ret = ret
        @TestFunction
        def foo():
            return 1
        
        # test
        result = foo()
        self.assertEqual(1, result)
        self.assertTrue(self.before_called)
        self.assertTrue(self.after_called)
        self.assertEqual(1, self.ret)
        
    def test_error(self):
        # set up
        class TestFunction(ContextFunction):
            def _before(self):
                CallTest.before_called = True
            def _error(self, error):
                CallTest.error_called = True
                CallTest.error = error
        @TestFunction
        def foo():
            raise Exception
        
        # test
        with self.assertRaises(Exception):
            foo()
        self.assertTrue(self.before_called)
        self.assertTrue(self.error_called)
        self.assertIsInstance(self.error, Exception)
        
class WithTest(TestCase):
    def test_success(self):
        # set up
        class TestFunction(ContextFunction):
            def _before(self, *args, **kw):
                WithTest.before_called = True
            def _after(self, ret, *args, **kw):
                WithTest.after_called = True
        
        # test
        with TestFunction():
            pass
        self.assertTrue(self.before_called)
        self.assertTrue(self.after_called)
        
    def test_error(self):
        # set up
        class TestFunction(ContextFunction):
            def _before(self, *args, **kw):
                WithTest.before_called = True
            def _error(self, error, *args, **kw):
                WithTest.error_called = True
                WithTest.error = error
        
        # test
        with self.assertRaises(Exception):
            with TestFunction():
                raise Exception()
        self.assertTrue(self.before_called)
        self.assertTrue(self.error_called)
        self.assertIsInstance(self.error, Exception)
        
    def test_init(self):
        # set up
        class TestFunction(ContextFunction):
            def _init(self, a):
                WithTest.a = a
        
        # test
        with TestFunction(1):
            pass
        self.assertEqual(1, self.a)
        