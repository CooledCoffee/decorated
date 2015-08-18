# -*- coding: utf-8 -*-
from decorated.base.function import WrapperFunction
from decorated.decorators.conditional import Conditional
from decorated.decorators.once import Once
from decorated.testing import DecoratedFixture
from fixtures2 import TestCase

class TestWrapperFunction(WrapperFunction):
    called = False
    
    def _before(self, *args, **kw):
        TestWrapperFunction.called = True
        
class DisableTest(TestCase):
    def setUp(self):
        super(DisableTest, self).setUp()
        self.decorated = self.useFixture(DecoratedFixture())
        
    def test_with_args(self):
        # set up
        @Conditional('a != 0')
        def foo(a):
            return a
        self.decorated.disable(Conditional)
        
        # test
        self.assertEqual(0, foo(0))
        self.assertEqual(1, foo(1))
        
    def test_no_arg(self):
        # set up
        DisableTest.args = []
        @Once
        def foo(a):
            DisableTest.args.append(a)
            return a
        self.decorated.disable(Once)
        
        # test
        self.assertEqual(1, foo(1))
        self.assertEqual(1, foo(1))
        self.assertEqual([1, 1], self.args)
        
    def test_method(self):
        # set up
        class Foo(object):
            @Conditional('a != 0')
            def bar(self, a):
                return a
        self.decorated.disable(Conditional)
        
        # test
        self.assertEqual(0, Foo().bar(0))
        self.assertEqual(1, Foo().bar(1))
        
    def test_wrapper_function(self):
        # set up
        @TestWrapperFunction
        def foo(a):
            return a
        self.decorated.disable(TestWrapperFunction)

        # test
        foo(0)
        self.assertFalse(TestWrapperFunction.called)
        
class EnableTest(TestCase):
    def test_with_args(self):
        # set up
        self.decorated = self.useFixture(DecoratedFixture())
        @Conditional('a != 0')
        def foo(a):
            return a
        self.decorated.disable(Conditional)
        self.decorated.enable(Conditional)
        
        # test
        self.assertIsNone(foo(0))
        self.assertEqual(1, foo(1))
        