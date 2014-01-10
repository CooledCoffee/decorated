# -*- coding: utf-8 -*-
from decorated.decorators.cache import SimpleCache
from unittest.case import TestCase

class CacheTest(TestCase):
    def test(self):
        # set up
        cache = SimpleCache()
        @cache.cache('/{id}')
        def foo(id):
            return id
        @cache.uncache('/{id}')
        def unfoo(id):
            pass
        
        # test
        self.assertEqual(0, len(cache._data))
        
        self.assertEqual(1, foo(1))
        self.assertEqual(1, len(cache._data))
        
        self.assertEqual(1, foo(1))
        self.assertEqual(1, len(cache._data))
        
        unfoo(1)
        self.assertEqual(0, len(cache._data))
        
        self.assertEqual(1, foo(1))
        self.assertEqual(1, len(cache._data))
        
        self.assertEqual(2, foo(2))
        self.assertEqual(2, len(cache._data))
        