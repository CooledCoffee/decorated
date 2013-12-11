# -*- coding: utf-8 -*-
from decorated.base.function import Function
from unittest.case import TestCase
import inspect

@Function
def foo(id, name='default name'):
    return '%s|%s' % (id, name)

class InitTest(TestCase):
    def test_no_arg(self):
        decorated = Function(foo)
        self.assertEquals(('id', 'name'), decorated.params)
        
    def test_with_args(self):
        decorated = Function(1, b=2)(foo)
        self.assertEquals(('id', 'name'), decorated.params)

class DecorateTest(TestCase):
    def test_single_level(self):
        self.assertEquals('foo', foo.__name__)
        self.assertEquals(('id', 'name'), foo.params)
        self.assertTrue(hasattr(foo, 'func_code') or hasattr(foo, '__code__'))
        self.assertEquals(('id', 'name'), foo.params)
        self.assertEquals(('id',), foo.required_params)
        self.assertEquals((('name','default name'),), foo.optional_params)
        
    def test_multi_levels(self):
        foo2 = Function(foo)
        self.assertEquals('foo', foo2.__name__)
        self.assertEquals(('id', 'name'), foo2.params)
        self.assertTrue(hasattr(foo2, 'func_code') or hasattr(foo2, '__code__'))
        
    def test_method(self):
        class Foo(object):
            def bar(self, a, b):
                pass
        self.assertEqual(('self', 'a', 'b'), Function(Foo.bar).params)
        self.assertEqual(('a', 'b'), Function(Foo().bar).params)
        
class TargetTest(TestCase):
    def test_raw_function(self):
        target = foo.target()
        self.assertTrue(inspect.isfunction(target))

    def test_function_wrapper(self):
        bar = Function(foo)
        target = bar.target()
        self.assertTrue(inspect.isfunction(target))
        
class GetAttrTest(TestCase):
    def test_found_in_decorator(self):
        class FooFunction(Function):
            def _init(self):
                self.foo = 'foo'
                
            def bar(self):
                return 'bar'
        @FooFunction
        def foo():
            pass
        self.assertEqual('foo', foo.foo)
        self.assertEqual('bar', foo.bar())
        
    def test_found_in_target(self):
        def foo():
            pass
        foo.foo = 'foo'
        foo.bar = lambda: 'bar'
        foo = Function(foo)
        self.assertEqual('foo', foo.foo)
        self.assertEqual('bar', foo.bar())
        
    def test_not_found(self):
        @Function
        def foo():
            pass
        with self.assertRaises(AttributeError):
            foo.foo
        with self.assertRaises(AttributeError):
            foo.bar()
            
    def test_not_decorated(self):
        with self.assertRaises(AttributeError):
            Function().foo
        with self.assertRaises(AttributeError):
            Function().bar()
        
class StrTest(TestCase):
    def test(self):
        s = str(foo)
        self.assertEquals('<Function base_test.function_test.function_test.foo>', s)

class ResolveArgsTest(TestCase):
    def test_simple(self):
        d = foo._resolve_args(1, name='my name')
        self.assertEquals(2, len(d))
        self.assertEquals(1, d['id'])
        self.assertEquals('my name', d['name'])
        
    def test_kw_as_args(self):
        d = foo._resolve_args(1, 'my name')
        self.assertEquals(2, len(d))
        self.assertEquals(1, d['id'])
        self.assertEquals('my name', d['name'])
        
    def test_arg_as_kw(self):
        d = foo._resolve_args(id=1, name='my name')
        self.assertEquals(2, len(d))
        self.assertEquals(1, d['id'])
        self.assertEquals('my name', d['name'])
        
    def test_default_arg(self):
        d = foo._resolve_args(1)
        self.assertEquals(2, len(d))
        self.assertEquals(1, d['id'])
        self.assertEquals('default name', d['name'])
        
    def test_missing_arg(self):
        with self.assertRaises(Exception):
            foo._resolve_args()
            
    def test_args(self):
        def foo(id, *args):
            pass
        decorated = Function(foo)
        d = decorated._resolve_args(1, 2, 3)
        self.assertEquals(1, len(d))
        self.assertEquals(1, d['id'])
            
    def test_kw(self):
        def foo(id, **kw):
            pass
        decorated = Function(foo)
        d = decorated._resolve_args(1, a=2)
        self.assertEquals(1, len(d))
        self.assertEquals(1, d['id'])
            
class EvaluateTest(TestCase):
    def test_success(self):
        result = foo._evaluate('str(id) + "-" + name', 1, name='my name')
        self.assertEquals('1-my name', result)
        
    def test_failed(self):
        with self.assertRaises(Exception):
            foo._evaluate('!@#$%', 1, name='my name')
        
class CallTest(TestCase):
    def test_no_init_arg(self):
        decorated = Function(foo)
        rslt = decorated('111', 'my name')
        self.assertEquals('111|my name', rslt)
        
    def test_with_init_args(self):
        decorated = Function(1, b=2)(foo)
        rslt = decorated('111', 'my name')
        self.assertEquals('111|my name', rslt)
        
    def test_args(self):
        def foo(id, *args):
            return args[0]
        decorated = Function(foo)
        result = decorated(1, 2, 3)
        self.assertEquals(2, result)
        
    def test_kw(self):
        def foo(id, **kw):
            return kw['a']
        decorated = Function(foo)
        result = decorated(1, a=2)
        self.assertEquals(2, result)
        