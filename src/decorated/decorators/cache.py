# -*- coding: utf-8 -*-
import time

from decorated.base.function import Function
from decorated.util import templates, modutil

class CacheDecorator(Function):
    @property
    def invalidate(self):
        return self._cache.uncache(self._key, **self._vars)
    
    def _call(self, *args, **kw):
        d = dict(self._vars)
        d.update(self._resolve_args(*args, **kw))
        key = self._key_template.eval(d)
        return self._process(key, *args, **kw)
        
    def _decorate(self, func):
        super(CacheDecorator, self)._decorate(func)
        var_names = self.params + tuple(self._vars.keys())
        self._key_template = templates.compile(self._key, var_names)
        return self

    def _init(self, cache, key, vars=None, options=None):
        super(CacheDecorator, self)._init()
        self._cache = cache
        self._key = key
        self._vars = vars or {}
        self._options = options
        
    def _process(self, key, *args, **kw):
        result = self._cache._get(key)
        if result is None:
            result = Function._call(self, *args, **kw)
            self._cache._set(key, result)
        return result
    
class Cache(object):
    def cache(self, key, vars=None, **options):
        class _Decorator(CacheDecorator):
            def _process(self, key, *args, **kw):
                result = self._cache._get(key, options)
                if result is None:
                    result = Function._call(self, *args, **kw)
                    self._cache._set(key, result, options)
                return result
        return _Decorator(self, key, vars=vars, options=options)
    
    def uncache(self, key, vars=None, **options):
        class _Decorator(CacheDecorator):
            def _process(self, key, *args, **kw):
                result = Function._call(self, *args, **kw)
                self._cache._delete(key, options)
                return result
        return _Decorator(self, key, vars=vars, options=options)
    
    def _delete(self, key):
        raise NotImplementedError()
    
    def _get(self, key):
        raise NotImplementedError()
    
    def _set(self, key, value):
        raise NotImplementedError()

class SimpleCache(Cache):
    def __init__(self):
        self._data = {}
        
    def _delete(self, key, options):
        del self._data[key]
        
    def _get(self, key, options):
        value, expires = self._data.get(key, (None, None))
        if expires is None or expires < time.time():
            return None
        else:
            return value
        
    def _set(self, key, value, options):
        expires = time.time() + options.get('ttl', 3600)
        self._data[key] = (value, expires)
        
if modutil.module_exists('pylru'):
    from pylru import lrucache
    
    class LruCache(Cache):
        def __init__(self, size=1000):
            self._cache = lrucache(size)
            
        def _delete(self, key, options):
            del self._cache[key]
        
        def _get(self, key, options):
            try:
                return self._cache[key]
            except KeyError:
                return None
        
        def _set(self, key, value, options):
            self._cache[key] = value
            