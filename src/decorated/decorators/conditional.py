# -*- coding: utf-8 -*-
from decorated.base.function import Function
from decorated.decorators.remove_extra_args import RemoveExtraArgs
import six

class Conditional(Function):
    def _call(self, *args, **kw):
        if self._test_condition(*args, **kw):
            return super(Conditional, self)._call(*args, **kw)
        
    def _init(self, condition):
        if isinstance(condition, six.string_types):
            self._condition = condition
        elif callable(condition):
            self._condition = RemoveExtraArgs(condition)
        else:
            raise Exception('Condition can only be string or callable.')
        
    def _test_condition(self, *args, **kw):
        d = self._resolve_args(*args, **kw)
        if 'self' in d:
            d['self_'] = d.pop('self')
        if isinstance(self._condition, six.string_types):
            return eval(self._condition, d)
        else:
            return self._condition(**d)
        