# -*- coding: UTF-8 -*-
from decorated.base.function import Function
from unittest.case import TestCase
import six

class MethodTest(TestCase):
    def test_single_level(self):
        # set up
        class Foo(object):
            @Function
            def bar(self, a, b=0):
                return a + b
            
        # test by class
        self.assertEqual(Foo, Foo.bar.im_class)
        self.assertIsNone(Foo.bar.im_self)
        self.assertIsNone(Foo.bar.__self__)
        self.assertEqual(('self', 'a', 'b'), Foo.bar.im_func.params)
        self.assertEqual(('self', 'a', 'b'), Foo.bar.__func__.params)
        self.assertEquals(3, Foo.bar(Foo(), 1, b=2))
        
        # test by instance
        foo = Foo()
        self.assertEqual(Foo, foo.bar.im_class)
        self.assertEqual(foo, foo.bar.im_self)
        self.assertEqual(foo, foo.bar.__self__)
        self.assertEqual(('self', 'a', 'b'), foo.bar.im_func.params)
        self.assertEqual(('self', 'a', 'b'), foo.bar.__func__.params)
        self.assertEquals(3, foo.bar(1, b=2))
        
    def test_multi_levels(self):
        # set up
        class Foo(object):
            @Function
            @Function
            def bar(self, a, b=0):
                return a + b
            
        # test by class
        self.assertEqual(Foo, Foo.bar.im_class)
        self.assertIsNone(Foo.bar.im_self)
        self.assertIsNone(Foo.bar.__self__)
        self.assertEqual(('self', 'a', 'b'), Foo.bar.im_func.params)
        self.assertEqual(('self', 'a', 'b'), Foo.bar.__func__.params)
        self.assertEquals(3, Foo.bar(Foo(), 1, b=2))
        
        # test by instance
        foo = Foo()
        self.assertEqual(Foo, foo.bar.im_class)
        self.assertEqual(foo, foo.bar.im_self)
        self.assertEqual(foo, foo.bar.__self__)
        self.assertEqual(('self', 'a', 'b'), foo.bar.im_func.params)
        self.assertEqual(('self', 'a', 'b'), foo.bar.__func__.params)
        self.assertEquals(3, foo.bar(1, b=2))
        
    def test_static_method(self):
        # set up
        class Foo(object):
            @staticmethod
            @Function
            def bar(a, b=0):
                return a + b
            
        # test
        self.assertEqual(('a', 'b'), Foo.bar.params)
        self.assertEquals(3, Foo.bar(1, b=2))
        
    def test_class_method(self):
        # set up
        class Foo(object):
            @classmethod
            @Function
            def bar(cls, a, b=0):
                return a + b
            
        # test
        if six.PY2:
            self.assertEqual(type, Foo.bar.im_class)
            self.assertEqual(Foo, Foo.bar.im_self)
            self.assertEqual(('cls', 'a', 'b'), Foo.bar.im_func.params)
        elif six.PY3:
            self.assertEqual(Foo, Foo.bar.__self__)
            self.assertEqual(('cls', 'a', 'b'), Foo.bar.__func__.params)
        else:
            self.fail()
        self.assertEquals(3, Foo.bar(1, b=2))
        
    def test_cache(self):
        class Foo(object):
            @Function
            def bar(self, a, b=0):
                return a + b
        self.assertEqual(Foo.bar, Foo.bar)
        foo = Foo()
        self.assertEqual(foo.bar, foo.bar)
        del foo
        self.assertEqual(0, len(Foo.bar._instance_cache))
        