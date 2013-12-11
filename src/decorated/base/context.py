# -*- coding: utf-8 -*-
from decorated.base.dict import Dict
from decorated.base.proxy import Proxy
from decorated.base.thread_local import ThreadLocal
import doctest

class Context(Dict):
    _CURRENT_CONTEXT = ThreadLocal()
    
    @staticmethod
    def current():
        ctx = Context._CURRENT_CONTEXT.get()
        if ctx:
            return ctx
        else:
            raise ContextError('Context should be set first.')
        
    def __init__(self, **kw):
        super(Context, self).__init__(**kw)
        self._old_ctx = None
        
    def __enter__(self):
        self._old_ctx = Context._CURRENT_CONTEXT.get()
        Context._CURRENT_CONTEXT.set(self)
        return self
    
    def __exit__(self, error_type, error_value, traceback):
        Context._CURRENT_CONTEXT.set(self._old_ctx)
        
    def dict(self):
        '''
        >>> ctx = Context(path='/test')
        >>> ctx.dict()
        {'path': '/test'}
        '''
        data = dict(self)
        del data['_old_ctx']
        return data
        
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
    