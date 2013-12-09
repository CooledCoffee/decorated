# -*- coding: utf-8 -*-
from decorated import compatibility
from decorated.function import Function

class conditional(Function):
    def _call(self, *args, **kw):
        func_kw = self._resolve_args(*args, **kw)
        if isinstance(self._condition, compatibility.STRING_TYPE):
            condition = eval(self._condition, func_kw)
        else:
            condition_kw = self._condition._resolve_args(**func_kw)
            condition = self._condition(**condition_kw)
        if condition:
            return super(conditional, self)._call(*args, **kw)

    def _condition(self):
        return True
    
    def _init(self, condition=None):
        if condition:
            if isinstance(condition, compatibility.STRING_TYPE):
                self._condition = condition
            elif callable(condition):
                self._condition = Function(condition)
            else:
                raise Exception('Condition can only be string or callable.')
        else:
            self._condition = Function(self._condition)
        