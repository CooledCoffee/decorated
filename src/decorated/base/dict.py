# -*- coding: utf-8 -*-
import doctest

class Dict(dict):
    '''
    >>> d = Dict(a=1)
    
    >>> 'a' in d
    True
    >>> d['a']
    1
    >>> d.a
    1
    
    >>> d.a = 2
    >>> d['a']
    2
    >>> d.a
    2
    
    >>> d['b'] = 2
    >>> 'b' in d
    True
    >>> d['b']
    2
    >>> d.b
    2
    
    >>> d.c = 3
    >>> 'c' in d
    True
    >>> d['c']
    3
    >>> d.c
    3
    
    >>> del d.c
    >>> 'c' in d
    False
    >>> d['c']
    Traceback (most recent call last):
    ...
    KeyError: 'c'
    >>> d.c
    Traceback (most recent call last):
    ...
    AttributeError: 'c'
    
    >>> del d.d
    Traceback (most recent call last):
    ...
    AttributeError: 'd'
    '''
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as e:
            raise AttributeError(str(e))
    
    def __setattr__(self, name, value): 
        self[name] = value
    
    def __delattr__(self, name):
        try:
            del self[name]
        except KeyError as e:
            raise AttributeError(str(e))
        
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
    