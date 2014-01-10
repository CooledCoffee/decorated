# -*- coding: utf-8 -*-
from decorated.base.context import Context, ctx, ContextError
from decorated.base.function import Function

class Once(Function):
    def _call(self, *args, **kw):
        key = self._evaluate_expression(self._key, *args, **kw)
        key = (self._func, key)
        try:
            results = ctx.once_results
        except ContextError:
            results = _DEFAULT_SESSION.once_results
        except AttributeError:
            results = _DEFAULT_SESSION.once_results
        if key in results:
            result = results[key]
        else:
            result = super(Once, self)._call(*args, **kw)
            results[key] = result
        return result
    
    def _init(self, key='None'):
        super(Once, self)._init()
        self._key = key
        
class OnceSession(Context):
    def __init__(self):
        super(OnceSession, self).__init__()
        self.once_results = {}
        
_DEFAULT_SESSION = OnceSession()
