# -*- coding: utf-8 -*-
from decorated.base.function import Function

class BaseDecorator(Function):
    def _init(self, cache, key):
        super(BaseDecorator, self)._init()
        self._cache = cache
        self._key = key
        
    def _decorate(self, func):
        super(BaseDecorator, self)._decorate(func)
        self._key = self._compile_template(self._key)
        return self

class Cache(object):
    def cache(self, key):
        class Decorator(BaseDecorator):
            def _call(self, *args, **kw):
                d = self._resolve_args(*args, **kw)
                key = self._key.eval(d)
                result = self._cache._get(key)
                if result is None:
                    result = super(Decorator, self)._call(*args, **kw)
                    self._cache._set(key, result)
                return result
        return Decorator(self, key)
    
    def uncache(self, key):
        class Decorator(BaseDecorator):
            def _call(self, *args, **kw):
                d = self._resolve_args(*args, **kw)
                key = self._key.eval(d)
                result = super(Decorator, self)._call(*args, **kw)
                self._cache._delete(key)
                return result
        return Decorator(self, key)
    
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
        