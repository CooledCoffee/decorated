# -*- coding: utf-8 -*-
from decorated.util.conditional import Conditional
from unittest.case import TestCase

class ConditionalTest(TestCase):
    def test_no_condition(self):
        @Conditional
        def foo(a, b):
            return a
        self.assertEqual(1, foo(1, 1))
        self.assertEqual(2, foo(2, 2))
        
    def test_method(self):
        class TestConditional(Conditional):
            def _condition(self, a):
                return a == 1
        @TestConditional
        def foo(a, b):
            return a
        self.assertEqual(1, foo(1, 1))
        self.assertIsNone(foo(2, 2))
        
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
        