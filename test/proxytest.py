# -*- coding: utf-8 -*-
from decorated.proxy import Proxy
from unittest.case import TestCase

class Target(object):
    def __init__(self):
        self.a = 1
        self.b = 1
    def foo(self):
        return 1
    def bar(self):
        return 1
    
class FakeProxy(Proxy):
    def __init__(self, target):
        super(FakeProxy, self).__init__(target)
        self.b = 2
    def bar(self):
        return 2

class ProxyTest(TestCase):
    def test_static_target(self):
        target = Target()
        proxy = FakeProxy(target)
        self.assertEquals(1, proxy.a)
        self.assertEquals(2, proxy.b)
        self.assertEquals(1, proxy.foo())
        self.assertEquals(2, proxy.bar())
        with self.assertRaises(AttributeError):
            proxy.c
        
    def test_dynamic_target(self):
        class FakeProxy(Proxy):
            def __init__(self):
                super(FakeProxy, self).__init__()
                self.b = 2
            def bar(self):
                return 2
            def _target(self):
                return Target()
        proxy = FakeProxy()
        self.assertEquals(1, proxy.a)
        self.assertEquals(2, proxy.b)
        self.assertEquals(1, proxy.foo())
        self.assertEquals(2, proxy.bar())
        with self.assertRaises(AttributeError):
            proxy.c
            
    def test_attr_not_found(self):
        # set up
        target = Target()
        proxy = FakeProxy(target)
        
        # test
        try:
            proxy.c
            self.fail()
        except AttributeError as e:
            self.assertEquals("'FakeProxy' object has no attribute 'c'", e.message)
            