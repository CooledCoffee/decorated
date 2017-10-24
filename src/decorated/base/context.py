# -*- coding: utf-8 -*-
import doctest
import logging

import six

from decorated.base.dict import Dict
from decorated.base.proxy import Proxy
from decorated.base.thread_local import ThreadLocal

log = logging.getLogger(__name__)

class ContextMeta(type):
    def __new__(mcs, name, bases, attrs):
        cls = type.__new__(mcs, name, bases, attrs)
        sub_class_enter = getattr(cls, '__enter__', None)
        def _enter(instance):
            result = instance
            if sub_class_enter is not None:
                result = sub_class_enter(instance)
            cls._current.set(instance) # pylint: disable=protected-access
            return result
        cls.__enter__ = _enter
        sub_class_exit = getattr(cls, '__exit__', None)
        def _exit(instance, *args, **kw):
            cls._current.set(None) # pylint: disable=protected-access
            if sub_class_exit is not None:
                sub_class_exit(instance, *args, **kw)
        cls.__exit__ = _exit
        cls._current = ThreadLocal() # pylint: disable=protected-access
        return cls
        
    def current(cls):
        return cls._current.get()
    
class Context(six.with_metaclass(ContextMeta, Dict)):
    def __init__(self, **kw):
        super(Context, self).__init__(**kw)
        self._defers = None
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
                log.warn('Failed to execute defer "%s".', defer)
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
        context = Context._current.get() # pylint: disable=protected-access
        if context is None:
            raise ContextError('Context should be set first.')
        return context

    def get(self):
        return self.target
        
class ContextError(Exception):
    pass

ctx = ContextProxy()

if __name__ == '__main__':
    doctest.testmod()
    