# -*- coding: utf-8 -*-
from decorated.base.dict import Dict
from decorated.base.proxy import Proxy
from decorated.base.thread_local import ThreadLocal
import doctest

class Context(Dict):
    _CURRENT_CONTEXT = ThreadLocal()
    
    def __init__(self, **kw):
        self._parent = Context._CURRENT_CONTEXT.get()
        fields = self._parent.dict() if self._parent else {}
        fields.update(kw)
        super(Context, self).__init__(**fields)
        self._pre_actions = []
        self._post_actions = []
        
    @staticmethod
    def current():
        ctx = Context._CURRENT_CONTEXT.get()
        if ctx:
            return ctx
        else:
            raise ContextError('Context should be set first.')
        
    def __enter__(self):
        Context._CURRENT_CONTEXT.set(self)
        return self
    
    def __exit__(self, error_type, error_value, traceback):
        Context._CURRENT_CONTEXT.set(self._parent)
                
    def dict(self):
        '''
        >>> ctx = Context(a=1, b=2, _c=3)
        >>> d = ctx.dict()
        >>> d['a']
        1
        >>> d['b']
        2
        >>> '_c' in d
        False
        '''
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
        return Context.current()
        
    def _target(self):
        return Context.current()
    
class ContextError(Exception):
    pass

ctx = ContextProxy()

if __name__ == '__main__':
    doctest.testmod()
    