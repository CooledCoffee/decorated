# -*- coding: utf-8 -*-
from decorated.base.context import Context, ctx
from decorated.decorators.cache import SimpleCache, LruCache
from unittest.case import TestCase

class SimpleCacheTest(TestCase):
    def test_get_set(self):
        cache = SimpleCache()
        self.assertIsNone(cache.get('a'))
        cache.set('a', 1)
        self.assertEquals(1, cache.get('a'))
        cache.delete('a')
        self.assertIsNone(cache.get('a'))

    def test_clear(self):
        cache = SimpleCache()
        cache.set('a', 1)
        cache.clear()
        self.assertIsNone(cache.get('a'))

class LruCacheTest(TestCase):
    def test_get_set(self):
        cache = LruCache()
        self.assertIsNone(cache.get('a'))
        cache.set('a', 1)
        self.assertEquals(1, cache.get('a'))
        cache.delete('a')
        self.assertIsNone(cache.get('a'))

    def test_clear(self):
        cache = LruCache()
        cache.set('a', 1)
        cache.clear()
        self.assertIsNone(cache.get('a'))
        
class CacheTest(TestCase):
    def setUp(self):
        super(CacheTest, self).setUp()
        self.cache = SimpleCache()
        self.calls = 0

    def test_simple(self):
        # set up
        @self.cache.cache('/{id}')
        def foo(id):
            self.calls += 1
            return id
        @self.cache.uncache('/{id}')
        def unfoo(id):
            return id
        
        # test
        self.assertEqual(0, len(self.cache._data))
        
        result = foo(1)
        self.assertEqual(1, result)
        self.assertEqual(1, self.calls)
        self.assertEqual(1, len(self.cache._data))
        
        self.assertEqual(1, foo(1))
        self.assertEqual(1, self.calls)
        self.assertEqual(1, len(self.cache._data))
        
        result = unfoo(1)
        self.assertEqual(1, result)
        self.assertEqual(0, len(self.cache._data))
        
        self.assertEqual(1, foo(1))
        self.assertEqual(2, self.calls)
        self.assertEqual(1, len(self.cache._data))
        
        self.assertEqual(2, foo(2))
        self.assertEqual(3, self.calls)
        self.assertEqual(2, len(self.cache._data))

    def test_ttl(self):
        # set up
        @self.cache.cache('/{id}', ttl=-1)
        def foo(id):
            self.calls += 1
            return id

        # test
        foo(1)
        self.assertEqual(1, self.calls)
        foo(1)
        self.assertEqual(2, self.calls)
        
    def test_extra_vars(self):
        # set up
        @self.cache.cache('/{a}/{ctx.b}', vars={'a': 1, 'ctx': ctx})
        def foo():
            pass
        @self.cache.uncache('/{a}/{ctx.b}', vars={'a': 1, 'ctx': ctx})
        def unfoo():
            pass
        with Context(b=2):
            foo()
            self.assertIn('/1/2', self.cache._data)
            unfoo()
            self.assertNotIn('/1/2', self.cache._data)
        
    def test_invalidate(self):
        # set up
        foo_cache = self.cache.cache('/{id}')
        @foo_cache
        def foo(id):
            pass
        @foo_cache.invalidate
        def unfoo(id):
            pass
        
        # test
        self.assertEqual(0, len(self.cache._data))
        
        foo(1)
        self.assertEqual(1, len(self.cache._data))
        
        unfoo(1)
        self.assertEqual(0, len(self.cache._data))
        