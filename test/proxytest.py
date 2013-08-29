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

class GetAttrTest(TestCase):
    def test_no_target(self):
        proxy = FakeProxy(None)
        try:
            proxy.a
        except Exception as e:
            self.assertEquals("FakeProxy has no target.", str(e))
        
    def test_target_attr(self):
        target = Target()
        proxy = FakeProxy(target)
        self.assertEquals(1, proxy.a)
        self.assertEquals(1, proxy.foo())
            
    def test_proxy_attr(self):
        target = Target()
        proxy = FakeProxy(target)
        self.assertEquals(2, proxy.b)
        self.assertEquals(2, proxy.bar())
            
    def test_attr_not_found(self):
        # set up
        target = Target()
        proxy = FakeProxy(target)
        
        # test
        try:
            proxy.c
            self.fail()
        except AttributeError as e:
            self.assertEquals("'FakeProxy' object has no attribute 'c'", str(e))
            
class HasAttrTest(TestCase):
    def test_no_target(self):
        proxy = FakeProxy(None)
        try:
            hasattr(proxy, 'a')
        except Exception as e:
            self.assertEquals("FakeProxy has no target.", str(e))
        
    def test_target_attr(self):
        target = Target()
        proxy = FakeProxy(target)
        self.assertTrue(hasattr(proxy, 'a'))
        self.assertTrue(hasattr(proxy, 'foo'))
             
    def test_proxy_attr(self):
        target = Target()
        proxy = FakeProxy(target)
        self.assertTrue(hasattr(proxy, 'b'))
        self.assertTrue(hasattr(proxy, 'bar'))
             
    def test_attr_not_found(self):
        target = Target()
        proxy = FakeProxy(target)
        self.assertFalse(hasattr(proxy, 'c'))
             