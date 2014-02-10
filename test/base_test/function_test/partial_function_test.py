# -*- coding: utf-8 -*-
from decorated.base.function import Function, PartialFunction
from unittest.case import TestCase

class FullDecorator(Function):
    def _init(self, a, b, c=None):
        self.a = a
        self.b = b
        self.c = c
    
def foo(d, e, f=None):
    return d + e + f

class InitTest(TestCase):
    def test_with_nothing(self):
        partial_decorator = PartialFunction(FullDecorator)
        decorated = partial_decorator(1, 2, 3)(foo)
        self.assertEqual(1, decorated.a)
        self.assertEqual(2, decorated.b)
        self.assertEqual(3, decorated.c)
        
    def test_with_args(self):
        partial_decorator = PartialFunction(FullDecorator, init_args=(1, 2))
        decorated = partial_decorator(3)(foo)
        self.assertEqual(1, decorated.a)
        self.assertEqual(2, decorated.b)
        self.assertEqual(3, decorated.c)
        
    def test_with_kw(self):
        partial_decorator = PartialFunction(FullDecorator, init_kw={'c': 3})
        decorated = partial_decorator(1, 2)(foo)
        self.assertEqual(1, decorated.a)
        self.assertEqual(2, decorated.b)
        self.assertEqual(3, decorated.c)

class CallTest(TestCase):
    def test_with_nothing(self):
        partial_decorator = PartialFunction(FullDecorator)
        decorated = partial_decorator(1, 2, 3)(foo)
        self.assertEqual(('d', 'e', 'f'), decorated.params)
        result = decorated(4, 5, 6)
        self.assertEqual(15, result)
        
    def test_with_args(self):
        partial_decorator = PartialFunction(FullDecorator, call_args=(4, 5))
        decorated = partial_decorator(1, 2, 3)(foo)
        self.assertEqual(('f',), decorated.params)
        result = decorated(6)
        self.assertEqual(15, result)
        
    def test_with_kw(self):
        partial_decorator = PartialFunction(FullDecorator, call_kw={'f': 6})
        decorated = partial_decorator(1, 2, 3)(foo)
        self.assertEqual(('d', 'e'), decorated.params)
        self.assertEqual(('d', 'e'), decorated.required_params)
        self.assertEqual((), decorated.optional_params)
        result = decorated(4, 5)
        self.assertEqual(15, result)
        