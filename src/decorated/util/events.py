# -*- coding: utf-8 -*-
from decorated import Function, util
from decorated.util.remove_extra_args import RemoveExtraArgs
from six import with_metaclass
import doctest

ENABLED = True
_INITED = False

class EventMetaType(type):
    def __init__(self, name, bases, attrs):
        super(EventMetaType, self).__init__(name, bases, attrs)
        self._sources = []
        self._after_listeners = []
        
    @property
    def name(self):
        return _get_full_name(self)
    
    @property
    def after(self):
        class _EventListener(EventListener):
            _event_class = self
        return _EventListener

class Event(with_metaclass(EventMetaType, Function)):
    fields = ()
    ret_field = None
    
    def _call(self, *args, **kw):
        ret = super(Event, self)._call(*args, **kw)
        if ENABLED:
            values = self._get_field_values(ret, *args, **kw)
            if self._condition(**values):
                self._trigger_listeners(values)
        return ret
    
    def _condition(self):
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
        self._condition = RemoveExtraArgs(self._condition)
    
    def _trigger_listeners(self, values):
        for listener in type(self)._after_listeners:
            listener._call(**values)
            
    def _validate(self):
        for field in self.fields:
            if field not in self.params:
                raise EventError('Missing field "%s" in "%s".' % (field, type(self).name))
        
class EventListener(RemoveExtraArgs):
    def _call(self, *args, **kw):
        if not ENABLED:
            return super(EventListener, self)._call(*args, **kw)
        return super(EventListener, self)._call(*args, **kw)
        
    def _decorate(self, func):
        super(EventListener, self)._decorate(func)
        self._validate()
        self._event_class._after_listeners.append(self)
        return self
    
    def _validate(self):
        for param in self.params:
            if param != self._event_class.ret_field and param not in self._event_class.fields:
                raise EventError('Event "%s" does not have field "%s".' % (self._event_class.name, param))
    
class EventError(Exception): pass

def init(packages):
    global _INITED
    if _INITED:
        return
    util.load_modules(packages)
    _INITED = True

def _get_full_name(func):
    '''
    >>> from decorated import util
    >>> _get_full_name(util.load_modules)
    'decorated.util.load_modules'
    '''
    return '%s.%s' % (func.__module__, func.__name__)

if __name__ == '__main__':
    doctest.testmod()
    