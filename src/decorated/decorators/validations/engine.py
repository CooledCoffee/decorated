# -*- coding: utf-8 -*-
from decorated import WrapperFunction
from decorated.decorators.validations.errors import ValidationError
from decorated.util import dutil


class ValidationEngine(object):
    def __init__(self, default_error_class=ValidationError):
        self._default_error_class = default_error_class

    def rules(self, validators, error_class=None):
        error_class = error_class or self._default_error_class
        return Rules(validators, error_class)

class Rules(WrapperFunction):
    def _before(self, *args, **kw):
        arg_dict = self._resolve_args(*args, **kw)
        for validator in self._validators:
            validator.validate(arg_dict, default_error_class=self._error_class)

    def _init(self, validators, error_class=None):
        super(Rules, self)._init()
        self._validators = dutil.listify(validators)
        self._error_class = error_class
        