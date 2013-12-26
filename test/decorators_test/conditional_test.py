# -*- coding: utf-8 -*-
from decorated.decorators.conditional import Conditional
from unittest.case import TestCase

class ConditionalTest(TestCase):
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
        
    def test_on_method(self):
        class Foo(object):
            @Conditional(condition=lambda a: a == 1)
            def bar(self, a):
                return a
        foo = Foo()
        self.assertEqual(1, foo.bar(1))
        self.assertIsNone(foo.bar(0))
        