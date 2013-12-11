# -*- coding: utf-8 -*-
import doctest

class Dict(dict):
    '''
    A Dict object is like a dictionary except `obj.foo` can be used
    in addition to `obj['foo']`.
    
    >>> o = Dict(a=1)
    >>> o.a
    1
    >>> o['a']
    1
    >>> o.a = 2
    >>> o['a']
    2
    >>> del o.a
    >>> o.a
    Traceback (most recent call last):
    ...
    AttributeError: 'a'
    >>> del o.b
    Traceback (most recent call last):
    ...
    AttributeError: 'b'
    '''
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k)
    
    def __setattr__(self, key, value): 
        self[key] = value
    
    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)
        
NOT_SET = object()

class DefaultDict(Dict):
    '''
    >>> d = DefaultDict(lambda k: 2 * k)
    >>> d['a']
    'aa'
    >>> 'a' in d
    True
    >>> d.b
    'bb'
    >>> 'b' in d
    True
    
    >>> d = DefaultDict()
    >>> d.a is None
    True
    
    >>> d = DefaultDict(a=1, b=2)
    >>> d.a
    1
    '''
    def __init__(self, default=None, **kw):
        super(DefaultDict, self).__init__(**kw)
        self._default = default or (lambda key: None)
        
    def __getattr__(self, key):
        return self.__getitem__(key)
    
    def __getitem__(self, key):
        if key not in self:
            self[key] = self._default(key)
        return super(DefaultDict, self).__getitem__(key)
    
if __name__ == '__main__':
    doctest.testmod()
    