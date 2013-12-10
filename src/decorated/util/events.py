# -*- coding: utf-8 -*-
from collections import defaultdict
from decorated import Function, util
from six import with_metaclass
import doctest

ENABLED = True
_INITED = False
_EVENTS = defaultdict(list)
_LISTENERS = defaultdict(list)

class EventMetaType(type):
    @property
    def full_name(self):
        return _get_full_name(self)
    
    @property
    def post(self):
        class _EventListener(EventListener):
            name = self.name
            _event_class = self
        return _EventListener

class BaseEvent(Function):
    name = None
    
    def _condition(self, ret, *args, **kw):
        return True
    
class Event(with_metaclass(EventMetaType, BaseEvent)):
    fields = ()
    ret_field = None
    
    def _call(self, *args, **kw):
        ret = super(Event, self)._call(*args, **kw)
        if ENABLED:
            if self._condition(ret, *args, **kw):
                self._trigger_listeners(ret, *args, **kw)
        return ret
    
    def _decorate(self, func):
        super(Event, self)._decorate(func)
        self._validate()
        _EVENTS[self.name].append(self)
        return self
    
    def _trigger_listeners(self, ret, *args, **kw):
        if self.ret_field:
            kw[self.ret_field] = ret
        for listener in _LISTENERS[self.name]:
            d = listener._resolve_args(*args, **kw)
            listener._call(**d)
            
    def _validate(self):
        for field in self.fields:
            if field not in self.params:
                raise EventError('Missing field "%s" in "%s".' % (field, type(self).full_name))
        
class EventListener(BaseEvent):
    def _call(self, *args, **kw):
        if not ENABLED:
            return super(EventListener, self)._call(*args, **kw)
        if self._condition(None, *args, **kw):
            return super(EventListener, self)._call(*args, **kw)
        
    def _decorate(self, func):
        super(EventListener, self)._decorate(func)
        self._validate()
        _LISTENERS[self.name].append(self)
        return self
    
    def _validate(self):
        for param in self.params:
            if param != self._event_class.ret_field and param not in self._event_class.fields:
                raise EventError('Event "%s" does not have field "%s".' % (self._event_class.full_name, param))
    
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
    