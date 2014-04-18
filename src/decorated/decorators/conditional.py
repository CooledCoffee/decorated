# -*- coding: utf-8 -*-
from decorated.base.function import Function
from decorated.decorators.remove_extra_args import RemoveExtraArgs
import six

class Conditional(Function):
    def _call(self, *args, **kw):
        if self._test(*args, **kw):
            return super(Conditional, self)._call(*args, **kw)
        
    def _init(self, condition=None):
        if hasattr(self, '_test'):
            _test = RemoveExtraArgs(self._test)
        elif isinstance(condition, six.string_types):
            def _test(*args, **kw):
                d = self._resolve_condition_args(*args, **kw)
                return eval(condition, d)
        elif callable(condition):
            condition = RemoveExtraArgs(condition)
            def _test(*args, **kw):
                d = self._resolve_condition_args(*args, **kw)
                return condition(**d)
        else:
            raise Exception('Condition can only be string or callable.')
        self._test = _test
        
    def _resolve_condition_args(self, *args, **kw):
        d = self._resolve_args(*args, **kw)
        if 'self' in d:
            d['self_'] = d.pop('self')
        return d
    