# -*- coding: utf-8 -*-
import six

from decorated.base.context import ContextError, ContextMeta
from decorated.base.false import NOTSET
from decorated.base.function import Function

class Once(Function):
    def _call(self, *args, **kw):
        key = self._evaluate_expression(self._key, *args, **kw)
        key = (self._func, key)

        try:
            values = OnceSession.current().values
        except ContextError:
            values = _DEFAULT_SESSION.values
        except AttributeError:
            values = _DEFAULT_SESSION.values

        value = values.get(key, NOTSET)
        if value == NOTSET:
            value = super(Once, self)._call(*args, **kw)
            values[key] = value
        return value
    
    def _init(self, key='None'): # pylint: disable=arguments-differ
        super(Once, self)._init()
        self._key = key
        
class OnceSession(six.with_metaclass(ContextMeta, object)):
    def __init__(self):
        super(OnceSession, self).__init__()
        self.values = {}
        
_DEFAULT_SESSION = OnceSession()
