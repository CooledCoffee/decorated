# -*- coding: UTF-8 -*-
import functools
import importlib
import inspect

from decorated.base.proxy import NoTargetError, Proxy

WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__doc__', '__code__', 'func_code')

class ArgError(Exception):
    def __init__(self, param, message):
        super(ArgError, self).__init__(message)
        self.param = param

class Function(Proxy): # pylint: disable=too-many-instance-attributes
    def __init__(self, *args, **kw):
        super(Function, self).__init__()
        self.params = None
        self.required_params = None
        self.optional_params = None
        self._func = None
        self._decorate_or_call = self._decorate
        if self._is_init_args(*args, **kw):
            self._init(*args, **kw)
        else:
            self._init()
            self._decorate(args[0])
            
    def __call__(self, *args, **kw):
        return self._decorate_or_call(*args, **kw)  
    
    def __get__(self, obj, cls):
        if obj is None:
            method = Function(self)
        else:
            method = partial(Function, call_args=(obj,))(self)
        method.im_class = cls # pylint: disable=attribute-defined-outside-init
        method.im_func = method.__func__ = self # pylint: disable=attribute-defined-outside-init
        method.im_self = method.__self__ = obj # pylint: disable=attribute-defined-outside-init
        return method
    
    def __str__(self):
        return '<Function %s.%s>' % (self._func.__module__, self.__name__)
    
    @property
    def func(self):
        return self._func.func if isinstance(self._func, Function) else self._func
    
    @property
    def target(self):
        if self._func is None:
            raise NoTargetError()
        return self._func
    
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

            # this is mainly for doctest purpose
            # doctest does not test on objects (Function instances)
            # so we put the original function back into the module
            mod = importlib.import_module(func.__module__)
            setattr(mod, '__original_%s' % func.__name__, func)
        self._decorate_or_call = self._call
        return self
    
    def _init(self, *args, **kw):
        pass
    
    def _is_init_args(self, *args, **kw): # pylint: disable=no-self-use
        return len(args) != 1 or not callable(args[0]) or len(kw) != 0
        
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
        results = {name: default for name, default in self.optional_params}
        for param, arg in zip(self.params, args):
            results[param] = arg
        results.update(kw)
        for name in self.params:
            if name not in results:
                msg = 'Missing argument "%s" for %s.' % (name, str(self))
                raise ArgError(name, msg)
        results = {k: v for k, v in results.items() if k in self.params}
        return results
    
class WrapperFunction(Function):
    def _call(self, *args, **kw):
        self._before(*args, **kw)
        try:
            result = super(WrapperFunction, self)._call(*args, **kw)
        except Exception as e:
            self._error(e, *args, **kw)
            raise
        else:
            self._after(result, *args, **kw)
        return result
    
    def _after(self, ret, *args, **kw):
        pass
    
    def _before(self, *args, **kw):
        pass
    
    def _error(self, error, *args, **kw):
        pass
    
class ContextFunction(WrapperFunction):
    def __enter__(self):
        self._before()
        return self
    
    def __exit__(self, error_type, error_value, traceback):
        if error_value is None:
            self._after(None)
        else:
            self._error(error_value)
    
def partial(func, init_args=(), init_kw=None, call_args=(), call_kw=None):
    if init_kw is None:
        init_kw = {}
    if call_kw is None:
        call_kw = {}
    class _PartialFunction(func): # pylint: disable=too-many-instance-attributes
        def __getattr__(self, name):
            attr = getattr(self._func, name)
            if callable(attr):
                method = attr
                def _wrapper(*args, **kw):
                    args = tuple(call_args) + args
                    merged_kw = dict(call_kw)
                    merged_kw.update(kw)
                    return method(*args, **merged_kw)
                attr = _wrapper
            return attr
        
        def __str__(self):
            return '<PartialFunction %s.%s>' % (self._func.__module__, self.__name__)
    
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
            self.params = self.params[len(call_args):] # pylint: disable=attribute-defined-outside-init
            self.required_params = self.params[len(call_args):] # pylint: disable=attribute-defined-outside-init
            self.params = tuple([p for p in self.params if p not in call_kw]) # pylint: disable=attribute-defined-outside-init
            self.required_params = tuple([p for p in self.required_params if p not in call_kw]) # pylint: disable=attribute-defined-outside-init
            self.optional_params = tuple([(k, v) for (k, v) in self.optional_params if k not in call_kw]) # pylint: disable=attribute-defined-outside-init
    return _PartialFunction
        
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
    return hasattr(func, '__self__') and func.__self__ is not None
