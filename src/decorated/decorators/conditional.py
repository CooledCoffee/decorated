# -*- coding: utf-8 -*-
from decorated.base.function import Function
from decorated.decorators.remove_extra_args import RemoveExtraArgs
import six

class Conditional(Function):
    def _call(self, *args, **kw):
        if self._test(*args, **kw):
            return super(Conditional, self)._call(*args, **kw)
        
    def _init(self, condition=None): # pylint: disable=arguments-differ
        if hasattr(self, '_test'):
            _test = RemoveExtraArgs(self._test) # pylint: disable=access-member-before-definition
        elif isinstance(condition, six.string_types):
            def _test(*args, **kw):
                arg_dict = self._resolve_condition_args(*args, **kw)
                return eval(condition, arg_dict) # pylint: disable=eval-used
        elif callable(condition):
            condition = RemoveExtraArgs(condition)
            def _test(*args, **kw):
                arg_dict = self._resolve_condition_args(*args, **kw)
                return condition(**arg_dict)
        else:
            raise Exception('Condition can only be string or callable.')
        self._test = _test
        
    def _resolve_condition_args(self, *args, **kw):
        arg_dict = self._resolve_args(*args, **kw)
        if 'self' in arg_dict:
            arg_dict['self_'] = arg_dict.pop('self')
        return arg_dict
    