# -*- coding: utf-8 -*-
from decorated.decorators.retries import Retries
from fixtures._fixtures.monkeypatch import MonkeyPatch
from fixtures2 import TestCase

class RetriesTest(TestCase):
    def test_success_at_first(self):
        @Retries(3)
        def foo():
            return 1
        result = foo()
        self.assertEqual(1, result)
        
    def test_success_after_retry(self):
        @Retries(3)
        def foo():
            foo.times += 1
            if foo.times == 3:
                return 1
            else:
                raise Exception('Failed at retry %d.' % foo.times)
        foo.times = 0
        result = foo()
        self.assertEqual(1, result)
        
    def test_all_failed(self):
        @Retries(3)
        def foo():
            foo.times += 1
            raise Exception()
        foo.times = 0
        with self.assertRaises(Exception):
            foo()
        self.assertEqual(3, foo.times)
        
    def test_invalid_times(self):
        with self.assertRaises(Exception):
            @Retries(0)
            def foo():
                pass
        with self.assertRaises(Exception):
            @Retries(-1)
            def bar():
                pass
            
    def test_disabled(self):
        self.useFixture(MonkeyPatch('decorated.decorators.retries.ENABLED', False))
        @Retries(3)
        def foo():
            foo.times += 1
            raise Exception()
        foo.times = 0
        with self.assertRaises(Exception):
            foo()
        self.assertEqual(1, foo.times)
        