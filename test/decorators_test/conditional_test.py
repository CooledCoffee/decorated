# -*- coding: utf-8 -*-
from decorated.decorators.conditional import Conditional
from fixtures2 import TestCase

class FunctionTest(TestCase):
    def test_string(self):
        @Conditional(condition='a == 1')
        def foo(a, b):
            return a
        self.assertEqual(1, foo(1, 1))
        self.assertIsNone(foo(2, 2))
        
    def test_lambda(self):
        @Conditional(condition=lambda a: a == 1)
        def foo(a, b):
            return a
        self.assertEqual(1, foo(1, 1))
        self.assertIsNone(foo(2, 2))
        
    def test_function(self):
        def _condition(a):
            return a == 1
        @Conditional(condition=_condition)
        def foo(a, b):
            return a
        self.assertEqual(1, foo(1, 1))
        self.assertIsNone(foo(2, 2))
        
    def test_sub_class(self):
        class TestConditional(Conditional):
            def _test(self, a):
                return a == 1
        @TestConditional
        def foo(a, b):
            return a
        self.assertEqual(1, foo(1, 1))
        self.assertIsNone(foo(2, 2))
        
class MethodTest(TestCase):
    def test_normal(self):
        class Foo(object):
            @Conditional(condition=lambda a: a == 1)
            def bar(self, a):
                return a
        foo = Foo()
        self.assertEqual(1, foo.bar(1))
        self.assertIsNone(foo.bar(0))
        
    def test_self_in_string(self):
        class Foo(object):
            def __init__(self, condition):
                self._condition = condition
                
            @Conditional(condition='self_._condition')
            def bar(self, a):
                return a
        foo = Foo(True)
        self.assertEqual(1, foo.bar(1))
        foo = Foo(False)
        self.assertIsNone(foo.bar(0))
        
    def test_self_in_lambda(self):
        class Foo(object):
            def __init__(self, condition):
                self._condition = condition
                
            @Conditional(condition=lambda self_: self_._condition)
            def bar(self, a):
                return a
        foo = Foo(True)
        self.assertEqual(1, foo.bar(1))
        foo = Foo(False)
        self.assertIsNone(foo.bar(0))
        
    def test_self_in_function(self):
        def _condition(self_):
            return self_._condition
        class Foo(object):
            def __init__(self, condition):
                self._condition = condition
                
            @Conditional(condition=_condition)
            def bar(self, a):
                return a
        foo = Foo(True)
        self.assertEqual(1, foo.bar(1))
        foo = Foo(False)
        self.assertIsNone(foo.bar(0))
        
    def test_self_in_sub_class(self):
        class TestConditional(Conditional):
            def _test(self, self_):
                return self_._condition
        class Foo(object):
            def __init__(self, condition):
                self._condition = condition
                
            @TestConditional
            def bar(self, a):
                return a
        foo = Foo(True)
        self.assertEqual(1, foo.bar(1))
        foo = Foo(False)
        self.assertIsNone(foo.bar(0))
        