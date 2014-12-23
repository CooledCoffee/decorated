# -*- coding: utf-8 -*-
from decorated.base.dict import Dict
from decorated.base.proxy import Proxy
from decorated.base.thread_local import ThreadLocal
import doctest
import logging

log = logging.getLogger(__name__)

class Context(Dict):
    _current = ThreadLocal()
    
    def __init__(self, **kw):
        super(Context, self).__init__(**kw)
        self._parent = Context._current.get()
        
    def __contains__(self, name):
        raise NotImplementedError()
        
    def __enter__(self):
        Context._current.set(self)
        self._defers = []
        return self
    
    def __exit__(self, error_type, error_value, traceback):
        for defer in self._defers:
            try:
                defer()
            except:
                log.warn('Failed to execute defer "%s".' % defer)
                pass
        Context._current.set(self._parent)
        
    def __getattr__(self, name):
        try:
            return super(Context, self).__getattr__(name)
        except AttributeError:
            if self._parent:
                try:
                    return getattr(self._parent, name)
                except AttributeError:
                    raise
            else:
                raise
            
    def __getitem__(self, name):
        raise NotImplementedError()
    
    def defer(self, action):
        self._defers.append(action)
        
    def dict(self):
        data = self._parent.dict() if self._parent else Dict()
        data.update({k: v for k, v in self.items() if not k.startswith('_')})
        return data
        
    def get(self, name, default=None):
        raise NotImplementedError()
            
class ContextProxy(Proxy):
    def __init__(self):
        super(ContextProxy, self).__init__()
        self._inited = True
        
    def __setattr__(self, name, value):
        if self.__dict__.get('_inited'):
            return setattr(self.target, name, value)
        else:
            self.__dict__[name] = value
    
    @property
    def target(self):
        ctx = Context._current.get()
        if ctx:
            return ctx
        else:
            raise ContextError('Context should be set first.')
    
    def get(self):
        return self.target
        
class ContextError(Exception):
    pass

ctx = ContextProxy()

if __name__ == '__main__':
    doctest.testmod()
    