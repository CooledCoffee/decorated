# -*- coding: utf-8 -*-
from decorated.base.function import Function, WrapperFunction
from decorated.decorators.once import Once
from decorated.decorators.remove_extra_args import RemoveExtraArgs
from decorated.util import modutil
from six import with_metaclass
import doctest

ENABLED = False

class EventMetaType(type):
    def __init__(self, name, bases, attrs):
        super(EventMetaType, self).__init__(name, bases, attrs)
        self._sources = []
        self._after_listeners = []
        self._before_listeners = []
        
    @property
    def after(self):
        class _EventListener(AfterEventListener):
            _event_class = self
        return _EventListener

    @property
    def before(self):
        class _EventListener(BeforeEventListener):
            _event_class = self
        return _EventListener

    @property
    def name(self):
        return _get_full_name(self)
    
class Event(with_metaclass(EventMetaType, WrapperFunction)):
    fields = ()
    ret_field = None
    
    @classmethod
    def fire(cls, data=None):
        if ENABLED:
            data = data or {}
            cls._execute_before_listeners(data)
            cls._execute_after_listeners(data)
            
    def _after(self, ret, error, *args, **kw):
        if not ENABLED:
            return
        data = self._get_field_values(ret, *args, **kw)
        self._execute_after_listeners(data)
            
    def _before(self, *args, **kw):
        if not ENABLED:
            return
        data = self._get_field_values(None, *args, **kw)
        self._execute_before_listeners(data)
    
    def _decorate(self, func):
        super(Event, self)._decorate(func)
        self._validate()
        type(self)._sources.append(self)
        return self
    
    def _get_field_values(self, ret, *args, **kw):
        values = self._resolve_args(*args, **kw)
        values = {k: v for k, v in values.items() if k in self.fields}
        if self.ret_field:
            values[self.ret_field] = ret
        return values
    
    @classmethod
    def _execute_after_listeners(cls, data):
        for listener in cls._after_listeners:
            listener._call(**data)
            
    @classmethod
    def _execute_before_listeners(cls, data):
        for listener in cls._before_listeners:
            listener._call(**data)
            
    def _validate(self):
        for field in self.fields:
            if field not in self.params:
                raise EventError('Missing field "%s" in "%s".' % (field, type(self).name))
        
class EventListener(RemoveExtraArgs):
    def _decorate(self, func):
        super(EventListener, self)._decorate(func)
        self._validate()
        self._register()
        return self
    
    def _register(self):
        raise NotImplemented()
    
    def _validate(self):
        for param in self.params:
            if param != self._event_class.ret_field and param not in self._event_class.fields:
                raise EventError('Event "%s" does not have field "%s".' % (self._event_class.name, param))
            
class AfterEventListener(EventListener):
    def _register(self):
        self._event_class._after_listeners.append(self)
    
class BeforeEventListener(EventListener):
    def _register(self):
        self._event_class._before_listeners.append(self)
    
class EventError(Exception):
    pass

@Once
def init(*packages):
    global ENABLED
    for p in packages:
        modutil.load_tree(p)
    ENABLED = True

def _get_full_name(func):
    '''
    >>> from decorated.util import modutil
    >>> _get_full_name(modutil.load_tree)
    'decorated.util.modutil.load_tree'
    '''
    return '%s.%s' % (func.__module__, func.__name__)

if __name__ == '__main__':
    doctest.testmod()
    