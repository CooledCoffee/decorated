# -*- coding: utf-8 -*-
from collections import Iterable

import re

import six

from decorated.base.function import WrapperFunction
from decorated.util import dutil


class ValidationError(Exception):
    pass

class ValidationEngine(object):
    def __init__(self, default_error_class=ValidationError):
        self._default_error_class = default_error_class

    def rules(self, validators, error_class=None):
        error_class = error_class or self._default_error_class
        return Rules(validators, error_class)
engine = ValidationEngine()

class Rules(WrapperFunction):
    def _before(self, *args, **kw):
        arg_dict = self._resolve_args(*args, **kw)
        for validator in self._validators:
            validator.validate(arg_dict, default_error_class=self._error_class)

    def _init(self, validators, error_class=None):
        super(Rules, self)._init()
        self._validators = dutil.listify(validators)
        self._error_class = error_class

class Validator(object):
    def __init__(self, param, error_class=None):
        self._param = param
        self._error_class = error_class

    def validate(self, arg_dict, default_error_class=None):
        value = arg_dict[self._param]
        error = self._validate(value)
        if error is not None:
            default_error_class = self._error_class or default_error_class
            e = default_error_class(error)
            e.param = self._param
            raise e

    def _format_value(self, value):
        '''
        >>> Validator(None)._format_value(111)
        '"111" (type=int)'
        >>> Validator(None)._format_value('111')
        '"111" (type=str)'
        '''
        return '"%s" (type=%s)' % (value, type(value).__name__)

    def _validate(self, value):
        raise NotImplementedError()

class IsInValidator(Validator):
    def __init__(self, param, values, error_class=None):
        super(IsInValidator, self).__init__(param, error_class=error_class)
        self._values = values

    def _validate(self, value):
        '''
        >>> IsInValidator('id', [1, 2, 3])._validate(2)

        >>> IsInValidator('id', [1, 2, 3])._validate(0)
        'Arg id should be one of [1, 2, 3], got "0" (type=int).'
        '''
        if value not in self._values:
            return 'Arg %s should be one of %s, got %s.' % (self._param, self._values, self._format_value(value))
is_in = IsInValidator

class NotNoneValidator(Validator):
    def _validate(self, value):
        '''
        >>> NotNoneValidator('id')._validate(111)

        >>> NotNoneValidator('id')._validate(None)
        'Arg id should not be none.'
        '''
        if value is None:
            return 'Arg %s should not be none.' % self._param
not_none = NotNoneValidator

class NotEmptyValidator(Validator):
    def _validate(self, value):
        '''
        >>> NotEmptyValidator('values')._validate(111)

        >>> NotEmptyValidator('values')._validate(None)
        'Arg values should not be empty, got "None" (type=NoneType).'

        >>> NotEmptyValidator('values')._validate([])
        'Arg values should not be empty, got "[]" (type=list).'

        >>> NotEmptyValidator('values')._validate('')
        'Arg values should not be empty, got "" (type=str).'
        '''
        if not value:
            return 'Arg %s should not be empty, got %s.' % (self._param, self._format_value(value))
not_empty = NotEmptyValidator

class OfTypeValidator(Validator):
    def __init__(self, param, types, error_class=None):
        super(OfTypeValidator, self).__init__(param, error_class=error_class)
        self._types = types
        if isinstance(types, Iterable):
            self._types_string = '(%s)' % ', '.join([t.__name__ for t in types])
        else:
            self._types_string = types.__name__

    def _validate(self, value):
        '''
        >>> OfTypeValidator('value', int)._validate(111)

        >>> OfTypeValidator('value', int)._validate('111')
        'Arg value should be int, got "111" (type=str).'

        >>> OfTypeValidator('value', (int, float))._validate('111')
        'Arg value should be (int, float), got "111" (type=str).'
        '''
        if not isinstance(value, self._types):
            return 'Arg %s should be %s, got %s.' % (self._param, self._types_string, self._format_value(value))
of_type = OfTypeValidator

class IsNumberValidator(OfTypeValidator):
    def __init__(self, param, error_class=None):
        super(IsNumberValidator, self).__init__(param, (int, float), error_class=error_class)
is_number = IsNumberValidator

class IsInRangeValidator(Validator):
    def __init__(self, param, lower, upper, error_class=None):
        super(IsInRangeValidator, self).__init__(param, error_class=error_class)
        self._lower = lower
        self._upper = upper

    def _validate(self, value):
        '''
        >>> IsInRangeValidator('score', 1, 10)._validate(5)

        >>> IsInRangeValidator('score', 1, 10)._validate(0)
        'Arg score should be within [1, 10], got 0.'

        >>> IsInRangeValidator('score', 1, 10)._validate(11)
        'Arg score should be within [1, 10], got 11.'
        '''
        if value < self._lower or value > self._upper:
            return 'Arg %s should be within [%s, %s], got %s.' % (self._param, self._lower, self._upper, value)
is_in_range = IsInRangeValidator

class IsPositiveValidator(IsNumberValidator):
    def _validate(self, value):
        '''
        >>> IsPositiveValidator('score')._validate(5)

        >>> IsPositiveValidator('score')._validate(-1)
        'Arg score should be positive, got "-1".'

        >>> IsPositiveValidator('score')._validate('aaa')
        'Arg score should be (int, float), got "aaa" (type=str).'
        '''
        error = super(IsPositiveValidator, self)._validate(value)
        if error is not None:
            return error

        if value < 0:
            return 'Arg %s should be positive, got "%s".' % (self._param, value)
is_positive = IsPositiveValidator

class NonNegativeValidator(IsNumberValidator):
    def _validate(self, value):
        '''
        >>> NonNegativeValidator('score')._validate(5)

        >>> NonNegativeValidator('score')._validate(0)
        'Arg score should be non negative, got "0".'

        >>> NonNegativeValidator('score')._validate('aaa')
        'Arg score should be (int, float), got "aaa" (type=str).'
        '''
        error = super(NonNegativeValidator, self)._validate(value)
        if error is not None:
            return error

        if value <= 0:
            return 'Arg %s should be non negative, got "%s".' % (self._param, value)
non_negative = NonNegativeValidator

class MaxLengthValidator(OfTypeValidator):
    def __init__(self, param, max_length, error_class=None):
        super(MaxLengthValidator, self).__init__(param, six.string_types, error_class=error_class)
        self._max_length = max_length

    def _validate(self, value):
        '''
        >>> MaxLengthValidator('name', 8)._validate('12345')

        >>> MaxLengthValidator('name', 8)._validate('123456789')
        'Arg name should be less than 8 chars, got "123456789".'

        >>> MaxLengthValidator('name', 8)._validate(123) is not None
        True
        '''
        error = super(MaxLengthValidator, self)._validate(value)
        if error is not None:
            return error

        if len(value) > self._max_length:
            return 'Arg %s should be less than %d chars, got "%s".' % (self._param, self._max_length, value)
max_length = MaxLengthValidator

class MatchRegexValidator(OfTypeValidator):
    def __init__(self, param, regex, error_class=None):
        super(MatchRegexValidator, self).__init__(param, six.string_types, error_class=error_class)
        self._regex = regex
        self._compiled_regex = re.compile(regex)

    def _validate(self, value):
        '''
        >>> MatchRegexValidator('name', '[a-z]+')._validate('aaa')

        >>> MatchRegexValidator('name', '[a-z]+')._validate('111')
        'Arg name should match regex "[a-z]+", got "111" (type=str).'

        >>> MatchRegexValidator('name', '[a-z]+')._validate(111) is not None
        True
        '''
        error = super(MatchRegexValidator, self)._validate(value)
        if error is not None:
            return error

        if not self._compiled_regex.match(value):
            return 'Arg %s should match regex "%s", got %s.' % (self._param, self._regex, self._format_value(value))
