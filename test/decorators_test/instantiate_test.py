# -*- coding: utf-8 -*-
from decorated.decorators.instantiate import Instantiate
from unittest.case import TestCase
import inspect

class InstantiateTest(TestCase):
    def test_default_call(self):
        @Instantiate
        class Foo(object):
            def __call__(self, a, b):
                return a + b
        self.assertEqual('Foo', Foo.__name__)
        self.assertEqual('decorators_test.instantiate_test', Foo.__module__)
        self.assertTrue(inspect.isclass(Foo.class_))
        result = Foo(1, b=2)
        self.assertEqual(3, result)
        
    def test_custom_call(self):
        @Instantiate('run')
        class Foo(object):
            def run(self, a, b):
                return a + b
        result = Foo(1, b=2)
        self.assertEqual(3, result)
        
    def test_callable(self):
        @Instantiate('run')
        class Foo(object):
            def __call__(self, a, b):
                return a * b
            
            def run(self, a, b):
                return a + b
        result = Foo(1, b=2)
        self.assertEqual(3, result)
        