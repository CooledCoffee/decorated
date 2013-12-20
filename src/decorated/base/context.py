# -*- coding: utf-8 -*-
from decorated.base.dict import Dict
from decorated.base.proxy import Proxy
from decorated.base.thread_local import ThreadLocal
import doctest

class Context(Dict):
    _current = ThreadLocal()
    
    def __init__(self, **kw):
        self._parent = Context._current.get()
        fields = self._parent.dict() if self._parent else {}
        fields.update(kw)
        super(Context, self).__init__(**fields)
        
    def __enter__(self):
        Context._current.set(self)
        return self
    
    def __exit__(self, error_type, error_value, traceback):
        Context._current.set(self._parent)
        
    def dict(self):
        return Dict({k: v for k, v in self.items() if not k.startswith('_')})
        
class ContextProxy(Proxy):
    def __init__(self):
        super(ContextProxy, self).__init__()
        self._inited = True
        
    def __setattr__(self, name, value):
        if self.__dict__.get('_inited'):
            target = self._target()
            return setattr(target, name, value)
        else:
            self.__dict__[name] = value
    
    def get(self):
        return self._target()
        
    def _target(self):
        ctx = Context._current.get()
        if ctx:
            return ctx
        else:
            raise ContextError('Context should be set first.')
    
class ContextError(Exception):
    pass

ctx = ContextProxy()

if __name__ == '__main__':
    doctest.testmod()
    