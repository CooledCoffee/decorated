# -*- coding: UTF-8 -*-
from decorated.base.function import Function
from unittest.case import TestCase

class MethodTest(TestCase):
    def test_instance_single_level(self):
        # set up
        class _Class(object):
            @Function
            def foo(self, id, name='default name'):
                return id
            
        # test
        ret = _Class().foo(111)
        self.assertEquals(111, ret)
        
    def test_instance_multi_levels(self):
        # set up
        class _Class(object):
            @Function
            @Function
            def foo(self, id, name='default name'):
                return id
            
        # test
        ret = _Class().foo(111)
        self.assertEquals(111, ret)
        
    def test_static_method(self):
        # set up
        class _Class(object):
            @staticmethod
            @Function
            def foo(id, name='default name'):
                return id
            
        # test
        self.assertEqual(111, _Class.foo(111))
        
    def test_class_method(self):
        # set up
        class _Class(object):
            @classmethod
            @Function
            def foo(cls, id, name='default name'):
                return id
            
        # test
        self.assertEqual(111, _Class.foo(111))
        
    def test_get_method(self):
        # set up
        class _Class(object):
            @Function
            def foo(self, id, name='default name'):
                return id
            
        # test
        self.assertIsInstance(_Class.foo, Function)
        