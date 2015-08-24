# -*- coding: utf-8 -*-
from decorated.decorators.events import Event, EventError, event
from fixtures2 import TestCase

class FooEvent(Event):
    fields = ('a', 'b')
    ret_field = 'z'
    
class ValidateTest(TestCase):
    def test_basic_fields(self):
        class TestEvent(Event):
            fields = ('a', 'b')
        @TestEvent
        def foo(a, b, c):
            pass
        
    def test_complex_fields(self):
        class TestEvent(Event):
            fields = ('a', 'b', 'c')
        @TestEvent(c='a + b')
        def foo(a, b):
            pass
        
    def test_failed(self):
        class TestEvent(Event):
            fields = ('a', 'b')
        with self.assertRaises(EventError):
            @TestEvent
            def foo(a):
                pass
    
class ListenerValidateTest(TestCase):
    def test_basic_fields(self):
        class TestEvent(Event):
            fields = ('a', 'b')
        @TestEvent.before
        def before(a):
            pass
        @TestEvent.after
        def after(a):
            pass
        
    def test_after_fields(self):
        class TestEvent(Event):
            fields = ('a', 'b')
            after_fields = ('c',)
        @TestEvent(c='ret')
        def foo(a, b):
            return a + b
        @TestEvent.before
        def before(a, b):
            pass
        @TestEvent.after
        def after(c):
            pass
        
    def test_failed(self):
        class TestEvent(Event):
            fields = ('a', 'b')
        with self.assertRaises(EventError):
            @TestEvent.before
            def before(a, b, c):
                pass
        with self.assertRaises(EventError):
            @TestEvent.after
            def after(a, b, c):
                pass
            
class CallTest(TestCase):
    def test_basic(self):
        # set up
        calls = []
        class TestEvent(Event):
            fields = ('a', 'b')
        @TestEvent
        def foo(a, b):
            return a + b
        @TestEvent.before
        def before(a, b):
            calls.append((a, b))
        @TestEvent.after
        def after(a, b):
            calls.append((a, b))
            
        # test
        result = foo(1, 2)
        self.assertEqual(3, result)
        self.assertEqual(2, len(calls))
        self.assertEqual((1, 2), calls[0])
        self.assertEqual((1, 2), calls[1])
        
    def test_complex_field(self):
        # set up
        calls = []
        class TestEvent(Event):
            fields = ('a', 'b', 'c')
        @TestEvent(c='a + b')
        def foo(a, b):
            return a + b
        @TestEvent.before
        def before(c):
            calls.append((c,))
        @TestEvent.after
        def after(c):
            calls.append((c,))
            
        # test
        foo(1, 2)
        self.assertEqual(2, len(calls))
        self.assertEqual((3,), calls[0])
        self.assertEqual((3,), calls[1])
        
    def test_after_fields(self):
        # set up
        calls = []
        class TestEvent(Event):
            fields = ('a', 'b')
            after_fields = ('c',)
        @TestEvent(c='ret')
        def foo(a, b):
            return a + b
        @TestEvent.before
        def before(a, b):
            calls.append((a, b))
        @TestEvent.after
        def after(c):
            calls.append((c,))
            
        # test
        foo(1, 2)
        self.assertEqual(2, len(calls))
        self.assertEqual((1, 2), calls[0])
        self.assertEqual((3,), calls[1])
    
class FireTest(TestCase):
    def test(self):
        # set up
        calls = []
        class TestEvent(Event):
            fields = ('a', 'b')
        @TestEvent.before
        def before(a, b):
            calls.append((a, b))
        @TestEvent.after
        def after(a, b):
            calls.append((a, b))
            
        # test
        TestEvent.fire({'a': 1, 'b': 2})
        self.assertEqual(2, len(calls))
        self.assertEqual((1, 2), calls[0])
        self.assertEqual((1, 2), calls[1])
        
class BuilderTest(TestCase):
    def test(self):
        # set up
        calls = []
        test_event = event(('a', 'b'))
        @test_event
        def foo(a, b):
            return a + b
        @test_event.before
        def before(a, b):
            calls.append((a, b))
        @test_event.after
        def after(a, b):
            calls.append((a, b))
            
        # test
        result = foo(1, 2)
        self.assertEqual(3, result)
        self.assertEqual(2, len(calls))
        self.assertEqual((1, 2), calls[0])
        self.assertEqual((1, 2), calls[1])
        