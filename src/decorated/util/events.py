# -*- coding: utf-8 -*-
from decorated import Function, util
from decorated.util.remove_extra_args import RemoveExtraArgs
from six import with_metaclass
import doctest

_ENABLED = False

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
    
class Event(with_metaclass(EventMetaType, Function)):
    fields = ()
    ret_field = None
    
    def _call(self, *args, **kw):
        if not _ENABLED:
            return super(Event, self)._call(*args, **kw)
        
        values = self._get_field_values(None, *args, **kw)
        self._trigger_before_listeners(values)
        
        ret = super(Event, self)._call(*args, **kw)
        
        values = self._get_field_values(ret, *args, **kw)
        self._trigger_after_listeners(values)
        
        return ret
    
    def _after_condition(self):
        return True
    
    def _before_condition(self):
        return True
    
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
    
    def _init(self):
        super(Event, self)._init()
        self._before_condition = RemoveExtraArgs(self._before_condition)
        self._after_condition = RemoveExtraArgs(self._after_condition)
    
    def _trigger_after_listeners(self, values):
        if self._after_condition(**values):
            for listener in type(self)._after_listeners:
                listener._call(**values)
            
    def _trigger_before_listeners(self, values):
        if self._before_condition(**values):
            for listener in type(self)._before_listeners:
                listener._call(**values)
            
    def _validate(self):
        for field in self.fields:
            if field not in self.params:
                raise EventError('Missing field "%s" in "%s".' % (field, type(self).name))
        
class EventListener(RemoveExtraArgs):
    def _call(self, *args, **kw):
        if not _ENABLED:
            return super(EventListener, self)._call(*args, **kw)
        return super(EventListener, self)._call(*args, **kw)
        
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
    
class EventError(Exception): pass

def init(packages):
    global _ENABLED
    if _ENABLED:
        return
    util.load_modules(packages)
    _ENABLED = True

def _get_full_name(func):
    '''
    >>> from decorated import util
    >>> _get_full_name(util.load_modules)
    'decorated.util.load_modules'
    '''
    return '%s.%s' % (func.__module__, func.__name__)

if __name__ == '__main__':
    doctest.testmod()
    