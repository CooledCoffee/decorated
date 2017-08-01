# -*- coding: utf-8 -*-
import time

from decorated.base.function import Function
from decorated.util import modutil, templates

class _CacheDecorator(Function):
    @property
    def invalidate(self):
        return self._cache.uncache(self._key, **self._vars)

    def _call(self, *args, **kw):
        arg_dict = dict(self._vars)
        arg_dict.update(self._resolve_args(*args, **kw))
        key = self._key_template.eval(arg_dict)
        return self._process(key, *args, **kw)

    def _decorate(self, func):
        super(_CacheDecorator, self)._decorate(func)
        var_names = self.params + tuple(self._vars.keys())
        self._key_template = templates.compile(self._key, var_names)
        return self

    def _init(self, cache, key, vars=None, options=None): # pylint: disable=arguments-differ
        super(_CacheDecorator, self)._init()
        self._cache = cache
        self._key = key
        self._vars = vars or {}
        self._options = options

    def _process(self, key, *args, **kw):
        raise NotImplementedError()

class Cache(object):
    def cache(self, key, vars=None, **options):
        class _Decorator(_CacheDecorator):
            def _process(self, key, *args, **kw):
                result = self._cache.get(key, **options)
                if result is None:
                    result = self._func(*args, **kw)
                    self._cache.set(key, result, **options)
                return result
        return _Decorator(self, key, vars=vars, options=options)

    def clear(self):
        raise NotImplementedError()
    
    def delete(self, key, **options):
        raise NotImplementedError()
    
    def get(self, key, **options):
        raise NotImplementedError()
    
    def set(self, key, value, **options):
        raise NotImplementedError()

    def uncache(self, key, vars=None, **options):
        class _Decorator(_CacheDecorator):
            def _process(self, key, *args, **kw):
                self._cache.delete(key, **options)
                return self._func(*args, **kw)
        return _Decorator(self, key, vars=vars, options=options)

class SimpleCache(Cache):
    def __init__(self):
        super(SimpleCache, self).__init__()
        self.clear()

    def clear(self):
        self._data = {}
        
    def delete(self, key, **options):
        del self._data[key]
        
    def get(self, key, **options):
        value, expires = self._data.get(key, (None, None))
        if expires is None or expires < time.time():
            return None
        else:
            return value
        
    def set(self, key, value, **options):
        expires = time.time() + options.get('ttl', 3600)
        self._data[key] = (value, expires)
        
if modutil.module_exists('pylru'):
    from pylru import lrucache
    
    class LruCache(Cache):
        def __init__(self, size=1000):
            self._size = size
            self.clear()

        def clear(self):
            self._cache = lrucache(self._size)
            
        def delete(self, key, **options):
            del self._cache[key]
        
        def get(self, key, **options):
            try:
                return self._cache[key]
            except KeyError:
                return None
        
        def set(self, key, value, **options):
            self._cache[key] = value
            