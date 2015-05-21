# -*- coding: utf-8 -*-
from decorated.base.context import Context, ctx
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
    def test_simple(self):
        # set up
        cache = SimpleCache()
        @cache.cache('/{id}')
        def foo(id):
            return id
        @cache.uncache('/{id}')
        def unfoo(id):
            return id
        
        # test
        self.assertEqual(0, len(cache._data))
        
        result = foo(1)
        self.assertEqual(1, result)
        self.assertEqual(1, len(cache._data))
        
        self.assertEqual(1, foo(1))
        self.assertEqual(1, len(cache._data))
        
        result = unfoo(1)
        self.assertEqual(1, result)
        self.assertEqual(0, len(cache._data))
        
        self.assertEqual(1, foo(1))
        self.assertEqual(1, len(cache._data))
        
        self.assertEqual(2, foo(2))
        self.assertEqual(2, len(cache._data))
        
    def test_extra_vars(self):
        # set up
        cache = SimpleCache()
        @cache.cache('/{a}/{ctx.b}', a=1, ctx=ctx)
        def foo():
            pass
        @cache.uncache('/{a}/{ctx.b}', a=1, ctx=ctx)
        def unfoo():
            pass
        with Context(b=2):
            foo()
            self.assertIn('/1/2', cache._data)
            unfoo()
            self.assertNotIn('/1/2', cache._data)
        
    def test_invalidate(self):
        # set up
        cache = SimpleCache()
        foo_cache = cache.cache('/{id}')
        @foo_cache
        def foo(id):
            pass
        @foo_cache.invalidate
        def unfoo(id):
            pass
        
        # test
        self.assertEqual(0, len(cache._data))
        
        foo(1)
        self.assertEqual(1, len(cache._data))
        
        unfoo(1)
        self.assertEqual(0, len(cache._data))
        