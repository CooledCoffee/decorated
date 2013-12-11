# -*- coding: utf-8 -*-
from decorated.base.proxy import Proxy
from unittest.case import TestCase

class TargetTest(TestCase):
    def test_static(self):
        target = object()
        proxied = Proxy(target)
        self.assertEqual(target, proxied._target())
        
    def test_dynamic(self):
        target = object()
        class DynamicProxy(Proxy):
            def _target(self):
                return target
        proxied = DynamicProxy()
        self.assertEqual(target, proxied._target())

class GetAttrTest(TestCase):
    def test_found_in_proxy(self):
        class Target(object):
            pass
        class TestProxy(Proxy):
            def __init__(self, target):
                super(TestProxy, self).__init__(target)
                self.foo = 'foo'
                
            def bar(self):
                return 'bar'
        proxy = TestProxy(Target())
        self.assertEqual('foo', proxy.foo)
        self.assertEqual('bar', proxy.bar())
        
    def test_found_in_target(self):
        class Target(object):
            def __init__(self):
                self.foo = 'foo'
                
            def bar(self):
                return 'bar'
        proxy = Proxy(Target())
        self.assertEqual('foo', proxy.foo)
        self.assertEqual('bar', proxy.bar())
        
    def test_not_found(self):
        class Target(object):
            pass
        proxy = Proxy(Target())
        with self.assertRaises(AttributeError):
            proxy.foo
        with self.assertRaises(AttributeError):
            proxy.bar()
            
    def test_no_target(self):
        proxy = Proxy()
        with self.assertRaises(AttributeError):
            proxy.foo
        with self.assertRaises(AttributeError):
            proxy.bar()
            