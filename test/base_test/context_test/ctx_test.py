# -*- coding: utf-8 -*-
from decorated.base.context import Context, ctx, ContextError
from unittest.case import TestCase

class GetSetAttrTest(TestCase):
    def test_set(self):
        with Context(a=1):
            self.assertEquals(1, ctx.a)
            ctx.a = 2
            self.assertEquals(2, ctx.a)
            ctx.b = 3
            self.assertEquals(3, ctx.b)
            d = ctx.dict()
            self.assertEquals({'a': 2, 'b': 3}, d)
        
class GetTest(TestCase):
    def test_success(self):
        with Context():
            self.assertIsInstance(ctx.get(), Context)
            
    def test_no_context(self):
        with self.assertRaises(ContextError):
            ctx.a
