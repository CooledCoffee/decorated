# -*- coding: utf-8 -*-
from decorated.base.function import Function
from decorated.util import templates

class BaseDecorator(Function):
    def _call(self, *args, **kw):
        d = dict(self._extra_vars)
        d.update(self._resolve_args(*args, **kw))
        key = self._key.eval(d)
        return self._process(key, *args, **kw)
        
    def _decorate(self, func):
        super(BaseDecorator, self)._decorate(func)
        var_names = self.params + tuple(self._extra_vars.keys())
        self._key = templates.compile(self._key, var_names)
        return self

    def _init(self, cache, key, extra_vars=None):
        super(BaseDecorator, self)._init()
        self._cache = cache
        self._key = key
        self._extra_vars = extra_vars or {}
        
    def _process(self, key, *args, **kw):
        raise NotImplementedError()
    
class Cache(object):
    def cache(self, key, **kw):
        class Decorator(BaseDecorator):
            def _process(self, key, *args, **kw):
                result = self._cache._get(key)
                if result is None:
                    result = Function._call(self, *args, **kw)
                    self._cache._set(key, result)
                return result
        return Decorator(self, key, extra_vars=kw)
    
    def uncache(self, key, **kw):
        class Decorator(BaseDecorator):
            def _process(self, key, *args, **kw):
                result = Function._call(self, *args, **kw)
                self._cache._delete(key)
                return result
        return Decorator(self, key, extra_vars=kw)
    
    def _delete(self, key):
        raise NotImplementedError()
    
    def _get(self, key):
        raise NotImplementedError()
    
    def _set(self, key, value):
        raise NotImplementedError()

class SimpleCache(Cache):
    def __init__(self):
        self._data = {}
        
    def _delete(self, key):
        del self._data[key]
        
    def _get(self, key):
        return self._data.get(key)
        
    def _set(self, key, value):
        self._data[key] = value
        
class LruCache(Cache):
    def __init__(self, size=1000):
        from pylru import lrucache
        self._cache = lrucache(size)
        
    def _delete(self, key):
        del self._cache[key]
    
    def _get(self, key):
        try:
            return self._cache[key]
        except KeyError:
            return None
    
    def _set(self, key, value):
        self._cache[key] = value
        