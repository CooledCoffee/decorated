# -*- coding: utf-8 -*-
from decorated.base.context import Context
from unittest.case import TestCase

class WithTest(TestCase):
    def test_single_level(self):
        with Context(path='/test'):
            self.assertEquals('/test', Context._current.get().path)
            
    def test_multi_levels(self):
        with Context(a=1, _a=1) as ctx1:
            self.assertEquals(1, ctx1.a)
            self.assertEquals(1, ctx1._a)
            with Context(b=2, _b=2) as ctx2:
                self.assertEquals(1, ctx2.a)
                self.assertEquals(2, ctx2.b)
                self.assertEquals(2, ctx2._b)
                with self.assertRaises(AttributeError):
                    ctx2._a
            self.assertEquals(1, ctx1.a)
            self.assertEquals(1, ctx1._a)
            with self.assertRaises(AttributeError):
                ctx1.b
        
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
                