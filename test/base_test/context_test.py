# -*- coding: UTF-8 -*-
from decorated.base.context import ctx, Context
from unittest.case import TestCase

class WithTest(TestCase):
    def test_simple(self):
        # no context
        with self.assertRaises(Exception):
            ctx.path
            
        # within context
        with Context(path='/test'):
            self.assertEquals('/test', ctx.path)
            self.assertIsInstance(ctx.get(), Context)
            
        # out of context
        with self.assertRaises(Exception):
            ctx.path
            
    def test_multi_levels(self):
        with Context(a=1, _a=1):
            self.assertEquals(1, ctx.a)
            self.assertEquals(1, ctx._a)
            with Context(b=2, _b=2):
                self.assertEquals(1, ctx.a)
                self.assertEquals(2, ctx.b)
                self.assertEquals(2, ctx._b)
                with self.assertRaises(AttributeError):
                    ctx._a
            self.assertEquals(1, ctx.a)
            self.assertEquals(1, ctx._a)
            with self.assertRaises(AttributeError):
                ctx.b
                
    def test_error_in_pre_actions(self):
        def _error():
            raise Exception()
        with self.assertRaises(Exception):
            with Context():
                ctx.register_pre_action(_error)
        self.assertIsNone(Context._CURRENT_CONTEXT.get())
        
class CtxTest(TestCase):
    def test_get(self):
        with Context(a=1):
            self.assertEquals(1, ctx.a)
            
    def test_set(self):
        with Context():
            ctx.a = 1
            self.assertEquals(1, Context.current().a)
        
    def test_get_context(self):
        with Context():
            self.assertEquals(Context.current(), ctx.get())
            
    def test_method(self):
        with Context(a=1):
            d = ctx.dict()
            self.assertEquals({'a': 1}, d)
