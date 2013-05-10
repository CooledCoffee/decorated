# -*- coding: UTF-8 -*-
from decorated.proxy import Proxy
import functools
import inspect

WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__doc__', '__code__', 'func_code')

class Function(Proxy):
    def __init__(self, *args, **kw):
        self.params = None
        self.required_params = None
        self.optional_params = None
        self._decorate_or_call = self._decorate
        if len(args) == 1 and callable(args[0]) and len(kw) == 0:
            self._init()
            self._decorate(args[0])
        else:
            self._init(*args, **kw)
            
    def __call__(self, *args, **kw):
        return self._decorate_or_call(*args, **kw)
    
    def __get__(self, instance, instancetype):
        if instance:
            # access within instance (e.g., Foo().bar)
            # wrap the current functor with Function1
            # no matter the current functor is Function1 or Function2
            return BoundedFunction(self, instance)
        else:
            # access in static way (e.g., Foo.bar)
            return self
    
    def __str__(self):
        return '<Function %s.%s>' % (self._func.__module__, self.__name__)
    
    def _call(self, *args, **kw):
        return self._func(*args, **kw)
    
    def _decorate(self, func):
        self._func = func
        functools.update_wrapper(self, func, WRAPPER_ASSIGNMENTS, updated=())
        if isinstance(func, Function):
            self.params = func.params
            self.required_params = func.required_params
            self.optional_params = func.optional_params
        else:
            self._parse_params(func)
        self._decorate_or_call = self._call
        return self
    
    def _evaluate(self, expression, *args, **kw):
        d = self._resolve_args(*args, **kw)
        return eval(expression, d)
        
    def _init(self, *args, **kw):
        pass
    
    def _parse_params(self, func):
        self.params, _, _, defaults = inspect.getargspec(func)
        if defaults:
            self.required_params = self.params[:-len(defaults)]
            self.optional_params = []
            for i in range(len(defaults) - 1, -1, -1):
                self.optional_params.append((self.params[-1 - i], defaults[-1 - i]))
        else:
            self.required_params = self.params
            self.optional_params = []
            
    def _resolve_args(self, *args, **kw):
        d = {name: default for name, default in self.optional_params}
        for param, arg in zip(self.params, args):
            d[param] = arg
        d.update(kw)
        for name in self.params:
            if name not in d:
                raise Exception('Missing argument "%s" for %s.' % (name, str(self)))
        d = {k: v for k, v in d.items() if k in self.params}
        return d
    
    def _target(self):
        return self._func
            
class BoundedFunction(Function):
    def __init__(self, func, instance):
        super(BoundedFunction, self).__init__(func)
        self._instance = instance
        
    def __call__(self, *args, **kw):
        args = [self._instance] + list(args)
        return self._func(*args, **kw)
        