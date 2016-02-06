# -*- coding: utf-8 -*-
from decorated.base.context import Context
from unittest.case import TestCase

class WithTest(TestCase):
    def test_single_level(self):
        with Context(path='/test'):
            self.assertEqual('/test', Context.current().path)
            
    def test_multi_levels(self):
        with Context(a=1, b=2):
            self.assertEqual(1, Context.current().a)
            self.assertEqual(2, Context.current().b)
            with Context(b=3, c=4):
                self.assertEqual(1, Context.current().a)
                self.assertEqual(3, Context.current().b)
                self.assertEqual(4, Context.current().c)
            self.assertEqual(1, Context.current().a)
            self.assertEqual(2, Context.current().b)
            with self.assertRaises(AttributeError):
                Context.current().c
            
    def test_multi_levels_method(self):
        class Context1(Context):
            def a(self):
                return 1
             
            def b(self):
                return 2
        class Context2(Context):
            def b(self):
                return 3
             
            def c(self):
                return 4
        with Context1():
            self.assertEqual(1, Context.current().a())
            self.assertEqual(2, Context.current().b())
            with Context2():
                self.assertEqual(1, Context.current().a())
                self.assertEqual(3, Context.current().b())
                self.assertEqual(4, Context.current().c())
            self.assertEqual(1, Context.current().a())
            self.assertEqual(2, Context.current().b())
            with self.assertRaises(AttributeError):
                self.assertEqual(3, Context.current().c())
        
class DictTest(TestCase):
    def test_single_level(self):
        ctx = Context(a=1, b=2, _c=3)
        data = ctx.dict()
        self.assertEqual({'a': 1, 'b': 2}, data)
        
    def test_multi_levels(self):
        with Context(a=1, b=2, _c=3):
            with Context(b=3, _d=4) as ctx:
                data = ctx.dict()
                self.assertEqual({'a': 1, 'b': 3}, data)
                
class DeferTest(TestCase):
    def test_normal(self):
        self.calls = []
        def _action1():
            self.calls.append('action1')
        def _action2():
            self.calls.append('action2')
        with Context() as ctx:
            ctx.defer(_action1)
            ctx.defer(_action2)
        self.assertEqual(['action1', 'action2'], self.calls)
        
    def test_error(self):
        self.calls = []
        def _action1():
            raise Exception
        def _action2():
            self.calls.append('action2')
        with Context() as ctx:
            ctx.defer(_action1)
            ctx.defer(_action2)
        self.assertEqual(['action2'], self.calls)
        