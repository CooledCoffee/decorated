# -*- coding: utf-8 -*-
from decorated.base import NOTSET
from decorated.base.function import WrapperFunction
from decorated.decorators.once import Once
from decorated.decorators.remove_extra_args import RemoveExtraArgs
from decorated.util import modutil
from six import with_metaclass
import doctest

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
    after_fields = ()
    
    @classmethod
    def fire(cls, data=None):
        data = data or {}
        cls._execute_before_listeners(data)
        cls._execute_after_listeners(data)
        
    @classmethod
    def _execute_after_listeners(cls, data):
        for listener in cls._after_listeners:
            listener._call(**data)
            
    @classmethod
    def _execute_before_listeners(cls, data):
        for listener in cls._before_listeners:
            listener._call(**data)
            
    def _after(self, ret, *args, **kw):
        data = self._get_field_values(ret, *args, **kw)
        self._execute_after_listeners(data)
        
    def _before(self, *args, **kw):
        data = self._get_field_values(NOTSET, *args, **kw)
        self._execute_before_listeners(data)
    
    def _decorate(self, func):
        super(Event, self)._decorate(func)
        self._validate()
        type(self)._sources.append(self)
        return self
    
    def _get_field_values(self, ret, *args, **kw):
        args = self._resolve_args(*args, **kw)
        values = {k: args[k] for k in self._basic_fields}
        for key, expression in self._complex_fields.items():
            values[key] = eval(expression, args)
        if ret != NOTSET:
            args['ret'] = ret
            for key, expression in self._after_complex_fields.items():
                values[key] = eval(expression, args)
        return values
    
    def _init(self, **complex_fields):
        super(Event, self)._init()
        self._complex_fields = {k: v for k, v in complex_fields.items() if k in self.fields}
        self._after_complex_fields = {k: v for k, v in complex_fields.items() if k in self.after_fields}
        self._basic_fields = [f for f in self.fields if f not in complex_fields]
    
    def _validate(self):
        for field in self._basic_fields:
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
        available_fields = self._get_available_fields()
        for param in self.params:
            if param not in available_fields:
                raise EventError('Event "%s" does not have field "%s".' % (self._event_class.name, param))
            
class AfterEventListener(EventListener):
    def _get_available_fields(self):
        return self._event_class.fields + self._event_class.after_fields
    
    def _register(self):
        self._event_class._after_listeners.append(self)
    
class BeforeEventListener(EventListener):
    def _get_available_fields(self):
        return self._event_class.fields
    
    def _register(self):
        self._event_class._before_listeners.append(self)
    
class EventError(Exception):
    pass

def event(fields, after_fields=()):
    fields_ = fields
    after_fields_ = after_fields
    class _Event(Event):
        fields = fields_
        after_fields = after_fields_
    return _Event

@Once
def init(*packages):
    for p in packages:
        modutil.load_tree(p)

def _get_full_name(func):
    '''
    >>> from decorated.util import modutil
    >>> _get_full_name(modutil.load_tree)
    'decorated.util.modutil.load_tree'
    '''
    return '%s.%s' % (func.__module__, func.__name__)

if __name__ == '__main__':
    doctest.testmod()
    