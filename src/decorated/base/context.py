# -*- coding: utf-8 -*-
from decorated.base.dict import Dict
from decorated.base.proxy import Proxy
from decorated.base.thread_local import ThreadLocal
from six import with_metaclass
import doctest
import logging

log = logging.getLogger(__name__)

class ContextMeta(type):
    def __new__(self, name, bases, attrs):
        cls = type.__new__(self, name, bases, attrs)
        sub_class_enter = getattr(cls, '__enter__', None)
        def _enter(instance):
            result = instance
            if sub_class_enter is not None:
                result = sub_class_enter(instance)
            cls._current.set(instance)
            return result
        cls.__enter__ = _enter
        sub_class_exit = getattr(cls, '__exit__', None)
        def _exit(instance, *args, **kw):
            cls._current.set(None)
            if sub_class_exit is not None:
                sub_class_exit(instance, *args, **kw)
        cls.__exit__ = _exit
        cls._current = ThreadLocal()
        return cls
        
    def current(self):
        return self._current.get()
    
class Context(with_metaclass(ContextMeta, Dict)):
    def __init__(self, **kw):
        super(Context, self).__init__(**kw)
        self._parent = None
        
    def __contains__(self, name):
        raise NotImplementedError()
        
    def __enter__(self):
        self._parent = Context.current()
        self._defers = []
        return self
    
    def __exit__(self, error_type, error_value, traceback):
        for defer in self._defers:
            try:
                defer()
            except Exception:
                log.warn('Failed to execute defer "%s".' % defer)
                pass
        Context._current.set(self._parent)
        
    def __getattr__(self, name):
        try:
            return super(Context, self).__getattr__(name)
        except AttributeError:
            if self._parent is None:
                raise
            else:
                try:
                    return getattr(self._parent, name)
                except AttributeError:
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
    