# -*- coding: utf-8 -*-
from decorated.base.function import ContextFunction
from fixtures2 import TestCase

class CallTest(TestCase):
    def test_success(self):
        # set up
        class TestFunction(ContextFunction):
            def _before(self):
                CallTest.before_called = True
            def _after(self, ret, error):
                CallTest.after_called = True
                CallTest.ret = ret
                CallTest.error = error
        @TestFunction
        def foo():
            return 1
        
        # test
        result = foo()
        self.assertEqual(1, result)
        self.assertTrue(self.before_called)
        self.assertTrue(self.after_called)
        self.assertEqual(1, self.ret)
        self.assertEqual(None, self.error)
        
    def test_error(self):
        # set up
        class TestFunction(ContextFunction):
            def _before(self):
                CallTest.before_called = True
            def _after(self, ret, error):
                CallTest.after_called = True
                CallTest.ret = ret
                CallTest.error = error
        @TestFunction
        def foo():
            raise Exception
        
        # test
        with self.assertRaises(Exception):
            foo()
        self.assertTrue(self.before_called)
        self.assertTrue(self.after_called)
        self.assertIsNone(self.ret)
        self.assertIsInstance(self.error, Exception)
        
class WithTest(TestCase):
    def test_success(self):
        # set up
        class TestFunction(ContextFunction):
            def _before(self, *args, **kw):
                WithTest.before_called = True
            def _after(self, ret, error, *args, **kw):
                WithTest.after_called = True
                WithTest.error = error
        
        # test
        with TestFunction():
            pass
        self.assertTrue(self.before_called)
        self.assertTrue(self.after_called)
        self.assertEqual(None, self.error)
        
    def test_error(self):
        # set up
        class TestFunction(ContextFunction):
            def _before(self, *args, **kw):
                WithTest.before_called = True
            def _after(self, ret, error, *args, **kw):
                WithTest.after_called = True
                WithTest.error = error
        
        # test
        with self.assertRaises(Exception):
            with TestFunction():
                raise Exception()
        self.assertTrue(self.before_called)
        self.assertTrue(self.after_called)
        self.assertIsInstance(self.error, Exception)
        
    def test_init(self):
        # set up
        class TestFunction(ContextFunction):
            def _init(self, a):
                WithTest.a = a
            def _before(self, *args, **kw):
                pass
            def _after(self, ret, error, *args, **kw):
                pass
        
        # test
        with TestFunction(1):
            pass
        self.assertEqual(1, self.a)
        