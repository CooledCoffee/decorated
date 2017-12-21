# -*- coding: utf-8 -*-

class Validator(object):
    def __init__(self, param, error_class=None):
        self._param = param
        self._error_class = error_class

    def validate(self, arg_dict, default_error_class=None):
        error_class = self._error_class or default_error_class
        value = self._eval_value(arg_dict, error_class)
        violation = self._validate(value)
        if violation is None:
            return
            
        e = error_class('Arg "%s" %s, got "%s" (type=%s).' % (self._param, violation, value, type(value).__name__))
        e.param = self._param
        raise e

    def _eval_value(self, arg_dict, error_class):
        if callable(self._param):
            try:
                value = self._param(**arg_dict)
            except Exception:
                raise error_class('Arg "%s" is missing or malformed.' % self._param)
        else:
            try:
                value = arg_dict[self._param]
            except KeyError:
                raise error_class('Arg "%s" is missing.' % self._param)
        return value

    def _validate(self, value):
        raise NotImplementedError()