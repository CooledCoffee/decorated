# -*- coding: utf-8 -*-
import doctest

from six import with_metaclass

from decorated.base.false import NOTSET
from decorated.base.function import WrapperFunction
from decorated.decorators.once import Once
from decorated.decorators.remove_extra_args import RemoveExtraArgs
from decorated.util import modutil


class EventError(Exception):
    pass

class EventListener(RemoveExtraArgs):
    def _decorate(self, func):
        super(EventListener, self)._decorate(func)
        self._validate()
        self._register()
        return self
    
    def _register(self):
        raise NotImplementedError()
    
    def _validate(self):
        available_fields = self._get_available_fields()
        for param in self.params:
            if param not in available_fields:
                raise EventError('Event "%s" does not have field "%s".' % (self._event_class.name, param))
            
class AfterEventListener(EventListener):
    def _get_available_fields(self):
        return self._event_class.fields + self._event_class.after_fields
    
    def _register(self):
        self._event_class._after_listeners.append(self) # pylint: disable=protected-access
    
class BeforeEventListener(EventListener):
    def _get_available_fields(self):
        return self._event_class.fields
    
    def _register(self):
        self._event_class._before_listeners.append(self) # pylint: disable=protected-access
    
class EventMetaType(type):
    def __init__(cls, name, bases, attrs):
        super(EventMetaType, cls).__init__(name, bases, attrs)
        cls._sources = []
        cls._after_listeners = []
        cls._before_listeners = []

    @property
    def after(cls):
        class _EventListener(AfterEventListener):
            _event_class = cls

        return _EventListener

    @property
    def before(cls):
        class _EventListener(BeforeEventListener):
            _event_class = cls

        return _EventListener

    @property
    def name(cls):
        return _get_full_name(cls)


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
            listener(**data)

    @classmethod
    def _execute_before_listeners(cls, data):
        for listener in cls._before_listeners:
            listener(**data)

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
            values[key] = eval(expression, args) # pylint: disable=eval-used
        if ret != NOTSET:
            args['ret'] = ret
            for key, expression in self._after_complex_fields.items():
                values[key] = eval(expression, args) # pylint: disable=eval-used
        return values

    def _init(self, **complex_fields): # pylint: disable=arguments-differ
        super(Event, self)._init()
        self._complex_fields = {k: v for k, v in complex_fields.items() if k in self.fields}
        self._after_complex_fields = {k: v for k, v in complex_fields.items() if k in self.after_fields}
        self._basic_fields = [f for f in self.fields if f not in complex_fields]

    def _validate(self):
        for field in self._basic_fields:
            if field not in self.params:
                raise EventError('Missing field "%s" in "%s".' % (field, type(self).name))

def event(fields, after_fields=()):
    fields_ = fields
    after_fields_ = after_fields
    class _Event(Event):
        fields = fields_
        after_fields = after_fields_
    return _Event

@Once
def init(*packages):
    for package in packages:
        modutil.load_tree(package)

def _get_full_name(func):
    '''
    >>> from decorated.util import modutil
    >>> _get_full_name(modutil.load_tree)
    'decorated.util.modutil.load_tree'
    '''
    return '%s.%s' % (func.__module__, func.__name__)

if __name__ == '__main__':
    doctest.testmod()
    