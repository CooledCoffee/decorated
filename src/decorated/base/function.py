# -*- coding: UTF-8 -*-
from decorated.base.proxy import Proxy
from decorated.util import templates
import doctest
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
    
    def target(self):
        return self._func.target() if isinstance(self._func, Function) else self._func
    
    def _call(self, *args, **kw):
        return self._func(*args, **kw)
    
    def _compile_template(self, template):
        return templates.compile(template, self.params)
    
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
    
    def _evaluate_expression(self, expression, *args, **kw):
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
            self.optional_params = ()
        if _is_bound_method(func):
            self.params = self.params[1:]
            self.required_params = self.required_params[1:]
        self.params = tuple(self.params)
        self.required_params = tuple(self.required_params)
        self.optional_params = tuple(self.optional_params)
        
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
    
def PartialFunction(func, init_args=(), init_kw=None, call_args=(), call_kw=None):
    if init_kw is None:
        init_kw = {}
    if call_kw is None:
        call_kw = {}
    class _PartialFunction(func):
        def _init(self, *args, **kw):
            args = tuple(init_args) + args
            kw.update(init_kw)
            super(_PartialFunction, self)._init(*args, **kw)
            
        def _call(self, *args, **kw):
            args = tuple(call_args) + args
            merged_kw = dict(call_kw)
            merged_kw.update(kw)
            return super(_PartialFunction, self)._call(*args, **merged_kw)
            
        def _parse_params(self, func):
            super(_PartialFunction, self)._parse_params(func)
            self.params = self.params[len(call_args):]
            self.required_params = self.params[len(call_args):]
            self.params = tuple([p for p in self.params if p not in call_kw])
            self.required_params = tuple([p for p in self.required_params if p not in call_kw])
            self.optional_params = tuple([(k, v) for (k, v) in self.optional_params if k not in call_kw])
    return _PartialFunction
        
def BoundedFunction(func, instance):
    return PartialFunction(Function, call_args=(instance,))(func)

def _is_bound_method(func):
    '''
    >>> def foo():
    ...     pass
    >>> _is_bound_method(foo)
    False
    
    >>> class Foo(object):
    ...     def bar(self):
    ...         pass
    >>> _is_bound_method(Foo.bar)
    False
    >>> _is_bound_method(Foo().bar)
    True
    '''
    try:
        return func.__self__ is not None
    except:
        return False

if __name__ == '__main__':
    doctest.testmod()
    