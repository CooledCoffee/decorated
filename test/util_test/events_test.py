# -*- coding: utf-8 -*-
from decorated.util.events import Event, EventError
from unittest.case import TestCase

class FooEvent(Event):
    fields = ('a', 'b')
    ret_field = 'z'
    
class EventTest(TestCase):
    def setUp(self):
        super(EventTest, self).setUp()
        FooEvent._sources = []
        FooEvent._after_listeners = []

class DecorateTest(EventTest):
    def test(self):
        @FooEvent
        def foo1(a, b):
            return 3
        @FooEvent
        def foo2(a, b):
            return 3
        @FooEvent.after
        def after_foo1(a):
            pass
        @FooEvent.after
        def after_foo2(z):
            pass
        self.assertEquals([foo1, foo2], FooEvent._sources)
        self.assertEquals([after_foo1, after_foo2], FooEvent._after_listeners)
        
class EventValidateTest(EventTest):
    def test_valid(self):
        @FooEvent
        def foo1(a, b):
            pass
        @FooEvent
        def foo2(a, b, c):
            pass
        
    def test_invalid(self):
        with self.assertRaises(EventError):
            @FooEvent
            def foo1(c):
                pass
        with self.assertRaises(EventError):
            @FooEvent
            def foo2(a):
                pass
            
    def test_empty_fields(self):
        @Event
        def foo(a, b):
            pass
            
class EventListenerValidateTest(EventTest):
    def test_valid(self):
        @FooEvent.after
        def after_foo1(a):
            pass
        @FooEvent.after
        def after_foo2(a, b):
            pass
        @FooEvent.after
        def after_foo3(a, z):
            pass
        @FooEvent.after
        def after_foo4(a, b, z):
            pass
        
    def test_invalid(self):
        with self.assertRaises(EventError):
            @FooEvent.after
            def after_foo1(c):
                pass
        with self.assertRaises(EventError):
            @FooEvent.after
            def after_foo2(a, b, z, c):
                pass
    
class CallTest(EventTest):
    def test_simple(self):
        self.called = []
        @FooEvent
        def foo(a, b):
            return a + b
        @FooEvent.before
        def before_foo(a):
            self.called.append(a)
        @FooEvent.after
        def after_foo1(a):
            self.called.append(a)
        @FooEvent.after
        def after_foo2(z):
            self.called.append(z)
        foo(1, 2)
        self.assertEquals([1, 1, 3], self.called)
        
    def test_conditional(self):
        # set up
        class ConditionalEvent(FooEvent):
            def _condition(self, a):
                return a == 2
        self.called = []
        @ConditionalEvent
        def foo(a, b):
            return a + b
        @ConditionalEvent.before
        def before_foo(a):
            self.called.append(a)
        @ConditionalEvent.after
        def after_foo1(a):
            self.called.append(a)
        @ConditionalEvent.after
        def after_foo2(z):
            self.called.append(z)
        
        # test
        foo(1, 1)
        self.assertEquals([], self.called)
        foo(2, 1)
        self.assertEquals([2, 2, 3], self.called)
        