# -*- coding: utf-8 -*-
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
