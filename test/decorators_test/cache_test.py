# -*- coding: utf-8 -*-
from decorated.decorators.cache import SimpleCache, LruCache
from unittest.case import TestCase

class SimpleCacheTest(TestCase):
    def test(self):
        cache = SimpleCache()
        self.assertIsNone(cache._get('a'))
        cache._set('a', 1)
        self.assertEquals(1, cache._get('a'))
        cache._delete('a')
        self.assertIsNone(cache._get('a'))

class LruCacheTest(TestCase):
    def test(self):
        cache = LruCache()
        self.assertIsNone(cache._get('a'))
        cache._set('a', 1)
        self.assertEquals(1, cache._get('a'))
        cache._delete('a')
        self.assertIsNone(cache._get('a'))
        
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
        