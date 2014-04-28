# -*- coding: utf-8 -*-
from decorated.base.context import Context
from decorated.decorators.once import Once, OnceSession
from fixtures._fixtures.monkeypatch import MonkeyPatch
from fixtures2 import TestCase

class DefaultSessionTest(TestCase):
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
        
    def test_disabled(self):
        self.useFixture(MonkeyPatch('decorated.decorators.once.ENABLED', False))
        @Once
        def foo(a, b):
            return a + b
        self.assertEqual(3, foo(1, 2))
        self.assertEqual(7, foo(3, 4))
        
class WithSessionTest(TestCase):
    def test_single_level(self):
        @Once
        def foo(a, b):
            return a + b
        with OnceSession():
            self.assertEqual(3, foo(1, 2))
        with OnceSession():
            self.assertEqual(7, foo(3, 4))
        
    def test_multi_levels(self):
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
                
    def test_context_is_not_session(self):
        @Once
        def foo(a, b):
            return a + b
        with Context():
            self.assertEqual(3, foo(1, 2))
            self.assertEqual(3, foo(3, 4))
            