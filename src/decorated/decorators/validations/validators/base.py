# -*- coding: utf-8 -*-

class Validator(object):
    def __init__(self, param, error_class=None):
        self._param = param
        self._error_class = error_class
        self._validator_classes = []
        self._validator_classes = _list_validator_classes(self.__class__)

    def validate(self, arg_dict, default_error_class=None):
        error_class = self._error_class or default_error_class
        value = self._eval_value(arg_dict, error_class)
        for cls in self._validator_classes:
            violation = cls._validate(self, value)
            if violation is not None:
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
    
def _list_validator_classes(cls):
    '''
    >>> class ParentValidator(Validator): pass
    >>> class ChildValidator(ParentValidator): pass
    >>> class GrandChildValidator(ChildValidator): pass
    >>> classes = _list_validator_classes(GrandChildValidator)
    >>> [c.__name__ for c in classes]
    ['ParentValidator', 'ChildValidator', 'GrandChildValidator']
    '''
    classes = []
    while issubclass(cls, Validator) and cls is not Validator:
        classes.append(cls)
        cls = cls.__bases__[0]
    return tuple(reversed(classes))
