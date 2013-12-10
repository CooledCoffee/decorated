# -*- coding: utf-8 -*-
from decorated.util import events
from decorated.util.events import Event, EventListener
from unittest.case import TestCase

class FooEvent(Event):
    name = 'foo'
    ret_var = 'c'
    
class EventTest(TestCase):
    def setUp(self):
        super(EventTest, self).setUp()
        events._EVENTS.clear()
        events._LISTENERS.clear()

class DecorateTest(EventTest):
    def test(self):
        @FooEvent(ret_var='c')
        def foo1(a, b):
            return 3
        @FooEvent(ret_var='c')
        def foo2(a, b):
            return 3
        @FooEvent.post
        def post_foo1(a):
            pass
        @FooEvent.post
        def post_foo2(c):
            pass
        self.assertEquals({'foo': [foo1, foo2]}, events._EVENTS)
        self.assertEquals({'foo': [post_foo1, post_foo2]}, events._LISTENERS)
        
class ValidateTest(EventTest):
    def test_valid(self):
        @FooEvent
        def foo1(a, b):
            return 3
        @FooEvent
        def foo2(a, b):
            return 3
        @FooEvent.post
        def post_foo1(a):
            pass
        @FooEvent.post
        def post_foo2(c):
            pass
        events._validate()
        
    def test_event_not_found(self):
        class PostFooEvent2(EventListener):
            name = 'foo2'
        @PostFooEvent2
        def post_foo2(a):
            pass
        with self.assertRaises(Exception):
            events._validate()
            
    def test_invalid_params(self):
        @FooEvent
        def foo(a, b):
            pass
        @FooEvent.post
        def post_foo(d):
            pass
        with self.assertRaises(Exception):
            events._validate()
            
class CallTest(EventTest):
    def test_simple(self):
        self.called = set()
        @FooEvent(ret_var='c')
        def foo(a, b):
            return 3
        @FooEvent.post
        def post_foo1(a):
            self.called.add(a)
        @FooEvent.post
        def post_foo2(c):
            self.called.add(c)
        foo(1, 2)
        self.assertEquals({1, 3}, self.called)
        
    def test_conditional_event(self):
        # set up
        class conditional_event(FooEvent):
            def _condition(self, ret, *args, **kw):
                return ret == 3
        called = set()
        @conditional_event(ret_var='c')
        def foo(a, b):
            return a + b
        @FooEvent.post
        def post_foo(a):
            called.add(a)
        
        # test
        foo(1, 1)
        self.assertEquals(set(), called)
        foo(2, 1)
        self.assertEquals({2}, called)
        
    def test_conditional_listener(self):
        # set up
        class conditional_post_event(FooEvent.post):
            def _condition(self, ret, a):
                return a == 2
        called = set()
        @FooEvent
        def foo(a, b):
            return 3
        @conditional_post_event
        def post_foo(a):
            called.add(a)
        
        # test
        foo(1, 1)
        self.assertEquals(set(), called)
        foo(2, 1)
        self.assertEquals({2}, called)
        