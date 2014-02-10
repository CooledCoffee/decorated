# -*- coding: utf-8 -*-
from decorated.base.function import Function
from decorated.util.templates import Template, TemplateError
from unittest.case import TestCase
import inspect

@Function
def foo(a, b=0):
    return a + b

class InitTest(TestCase):
    def test_no_arg(self):
        class _decorator(Function):
            def _init(self):
                self.inited = True
        @_decorator
        def foo():
            pass
        self.assertTrue(foo.inited)
        
    def test_with_args(self):
        class _decorator(Function):
            def _init(self, a, b=0):
                self.a = a
                self.b = b
        @_decorator(1, b=2)
        def foo():
            pass
        self.assertEqual(1, foo.a)
        self.assertEqual(2, foo.b)
        
class DecorateTest(TestCase):
    def test_no_init_args(self):
        @Function
        def foo(a, b=0):
            pass
        self.assertEquals('foo', foo.__name__)
        self.assertTrue(hasattr(foo, 'func_code') or hasattr(foo, '__code__'))
        self.assertEquals(('a', 'b'), foo.params)
        self.assertEquals(('a',), foo.required_params)
        self.assertEquals((('b',0),), foo.optional_params)
        self.assertEqual(foo._call, foo._decorate_or_call)
        
    def test_with_init_args(self):
        @Function(1)
        def foo(a, b=0):
            pass
        self.assertEquals('foo', foo.__name__)
        self.assertTrue(hasattr(foo, 'func_code') or hasattr(foo, '__code__'))
        self.assertEquals(('a', 'b'), foo.params)
        self.assertEquals(('a',), foo.required_params)
        self.assertEquals((('b',0),), foo.optional_params)
        self.assertEqual(foo._call, foo._decorate_or_call)
        
    def test_multi_levels(self):
        @Function
        @Function
        def foo(a, b=0):
            pass
        self.assertEquals('foo', foo.__name__)
        self.assertTrue(hasattr(foo, 'func_code') or hasattr(foo, '__code__'))
        self.assertEquals(('a', 'b'), foo.params)
        self.assertEquals(('a',), foo.required_params)
        self.assertEquals((('b',0),), foo.optional_params)
        
class TargetTest(TestCase):
    def test_raw_function(self):
        @Function
        def foo():
            pass
        target = foo.target()
        self.assertTrue(inspect.isfunction(target))
        
    def test_function_wrapper(self):
        @Function
        @Function
        def foo():
            pass
        target = foo.target()
        self.assertTrue(inspect.isfunction(target))
        
class StrTest(TestCase):
    def test(self):
        s = str(foo)
        self.assertEquals('<Function base_test.function_test.function_test.foo>', s)
        
class ResolveArgsTest(TestCase):
    def test_simple(self):
        d = foo._resolve_args(1, b=2)
        self.assertEquals(2, len(d))
        self.assertEquals(1, d['a'])
        self.assertEquals(2, d['b'])
        
    def test_default_arg(self):
        d = foo._resolve_args(1)
        self.assertEquals(2, len(d))
        self.assertEquals(1, d['a'])
        self.assertEquals(0, d['b'])
        
    def test_kw_as_args(self):
        d = foo._resolve_args(1, 2)
        self.assertEquals(2, len(d))
        self.assertEquals(1, d['a'])
        self.assertEquals(2, d['b'])
        
    def test_arg_as_kw(self):
        d = foo._resolve_args(a=1, b=2)
        self.assertEquals(2, len(d))
        self.assertEquals(1, d['a'])
        self.assertEquals(2, d['b'])
        
    def test_missing_arg(self):
        with self.assertRaises(Exception):
            foo._resolve_args()
            
class EvaluateExpressionTest(TestCase):
    def test_success(self):
        result = foo._evaluate_expression('a + b', 1, b=2)
        self.assertEquals(3, result)
        
    def test_failed(self):
        with self.assertRaises(Exception):
            foo._evaluate_expression('!@#$%', 1, b=2)
            
class CompileTemplateTest(TestCase):
    def test_success(self):
        template = foo._compile_template('A is {a}.')
        self.assertIsInstance(template, Template)
        
    def test_failed(self):
        with self.assertRaises(TemplateError):
            foo._compile_template('C is {c}.')
        
class CallTest(TestCase):
    def test_no_init_arg(self):
        result = foo(1, b=2)
        self.assertEqual(3, result)
        