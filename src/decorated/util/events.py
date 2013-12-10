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
    def post(self):
        class _EventListener(EventListener):
            name = self.name
        return _EventListener

class BaseEvent(Function):
    name = None
    
    def _condition(self, ret, *args, **kw):
        return True
    
class Event(with_metaclass(EventMetaType, BaseEvent)):
    ret_var = None
    
    def _call(self, *args, **kw):
        ret = super(Event, self)._call(*args, **kw)
        if ENABLED:
            if self._condition(ret, *args, **kw):
                self._trigger_listeners(ret, *args, **kw)
        return ret
    
    def _decorate(self, func):
        _EVENTS[self.name].append(self)
        return super(Event, self)._decorate(func)
    
    def _trigger_listeners(self, ret, *args, **kw):
        if self.ret_var:
            kw[self.ret_var] = ret
        for listener in _LISTENERS[self.name]:
            d = listener._resolve_args(*args, **kw)
            listener._call(**d)
        
class EventListener(BaseEvent):
    def _call(self, *args, **kw):
        if not ENABLED:
            return super(EventListener, self)._call(*args, **kw)
        if self._condition(None, *args, **kw):
            return super(EventListener, self)._call(*args, **kw)
        
    def _decorate(self, func):
        _LISTENERS[self.name].append(self)
        return super(EventListener, self)._decorate(func)
    
def init(packages):
    global _INITED
    if not _INITED:
        util.load_modules(packages)
        _validate()
        _INITED = True

def _get_full_name(func):
    '''
    >>> from decorated import util
    >>> _get_full_name(util.load_modules)
    'decorated.util.load_modules'
    '''
    return '%s.%s' % (func.__module__, func.__name__)

def _validate():
    _validate_events()
    _validate_listeners()
    
def _validate_events():
    for name, events in _EVENTS.items():
        for Event in events:
            if Event.ret_var != events[0].ret_var:
                raise Exception('There are multi definitions of Event %s which are not consistent.' % name)
    
def _validate_listeners():
    for event_name, listeners in _LISTENERS.items():
        if event_name not in _EVENTS:
            raise Exception('Event %s not found.' % event_name)
        Event = _EVENTS[event_name][0]
        allowed_params = Event.params + (Event.ret_var,) # ok even if _ret_var is None
        for listener in listeners:
            for param in listener.params:
                if param not in allowed_params:
                    raise Exception('Event listener %s refer to param %s which is not presented in Event %s.' \
                            % (_get_full_name(listener), param, event_name))

if __name__ == '__main__':
    doctest.testmod()
    