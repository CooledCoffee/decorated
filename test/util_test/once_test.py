# -*- coding: utf-8 -*-
from decorated.base.context import Context
from decorated.util.once import Once, OnceSession
from unittest.case import TestCase

class OnceTest(TestCase):
    def test_no_key(self):
        @Once
        def foo(a, b):
            return a + b
        self.assertEqual(3, foo(1, 2))
        self.assertEqual(3, foo(3, 4))
        
    def test_with_key(self):
        @Once('a')
        def foo(a, b):
            return a + b
        self.assertEqual(3, foo(1, 2))
        self.assertEqual(7, foo(3, 4))
        self.assertEqual(3, foo(1, 2))
        
    def test_diff_funcs(self):
        @Once
        def add(a, b):
            return a + b
        @Once
        def mul(a, b):
            return a * b
        self.assertEqual(3, add(1, 2))
        self.assertEqual(2, mul(1, 2))
        
    def test_with_session(self):
        @Once
        def foo(a, b):
            return a + b
        with OnceSession():
            self.assertEqual(3, foo(1, 2))
        with OnceSession():
            self.assertEqual(7, foo(3, 4))
        
    def test_with_multi_level_context(self):
        @Once
        def foo(a, b):
            return a + b
        with Context():
            with OnceSession():
                with Context():
                    self.assertEqual(3, foo(1, 2))
            with OnceSession():
                with Context():
                    self.assertEqual(7, foo(3, 4))
                