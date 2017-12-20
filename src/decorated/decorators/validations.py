# -*- coding: utf-8 -*-
import re
from collections import Iterable

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
        violation = self._validate(value)
        if violation is not None:
            error_class = self._error_class or default_error_class
            msg = 'Arg "%s" %s, got "%s" (type=%s).' % (self._param, violation, value, type(value).__name__)
            e = error_class(msg)
            e.param = self._param
            raise e

    def _validate(self, value):
        raise NotImplementedError()

class IsInValidator(Validator):
    def __init__(self, param, choices, error_class=None):
        super(IsInValidator, self).__init__(param, error_class=error_class)
        self._choices = choices

    def _validate(self, value):
        '''
        >>> IsInValidator('id', [1, 2, 3])._validate(2)
        >>> IsInValidator('id', [1, 2, 3])._validate(0)
        'should be one of [1, 2, 3]'
        '''
        if value not in self._choices:
            return 'should be one of %s' % self._choices
is_in = IsInValidator

class NotNoneValidator(Validator):
    def _validate(self, value):
        '''
        >>> NotNoneValidator('id')._validate(111)
        >>> NotNoneValidator('id')._validate(None)
        'should not be none'
        '''
        if value is None:
            return 'should not be none'
not_none = NotNoneValidator

class NotEmptyValidator(Validator):
    def _validate(self, value):
        '''
        >>> NotEmptyValidator('values')._validate(111)
        >>> NotEmptyValidator('values')._validate(None)
        'should not be empty'
        >>> NotEmptyValidator('values')._validate([])
        'should not be empty'
        >>> NotEmptyValidator('values')._validate('')
        'should not be empty'
        '''
        if not value:
            return 'should not be empty'
not_empty = NotEmptyValidator

class OfTypeValidator(Validator):
    def __init__(self, param, types, error_class=None):
        super(OfTypeValidator, self).__init__(param, error_class=error_class)
        self._types = types
        if isinstance(types, Iterable):
            self._types_string = '/'.join([t.__name__ for t in types])
        else:
            self._types_string = types.__name__

    def _validate(self, value):
        '''
        >>> OfTypeValidator('value', int)._validate(111)
        >>> OfTypeValidator('value', int)._validate('111')
        'should be int'
        >>> OfTypeValidator('value', (int, float))._validate('111')
        'should be int/float'
        '''
        if not isinstance(value, self._types):
            return 'should be %s' % self._types_string
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
        number value
        >>> IsInRangeValidator('score', 1, 10)._validate(5)
        >>> IsInRangeValidator('score', 1, 10)._validate(0)
        'should be in range [1, 10]'
        >>> IsInRangeValidator('score', 1, 10)._validate(11)
        'should be in range [1, 10]'

        string value
        >>> IsInRangeValidator('rank', 'A', 'D')._validate('B')
        >>> IsInRangeValidator('rank', 'A', 'D')._validate('E')
        'should be in range [A, D]'
        '''
        if value < self._lower or value > self._upper:
            return 'should be in range [%s, %s]' % (self._lower, self._upper)
is_in_range = IsInRangeValidator

class IsPositiveValidator(IsNumberValidator):
    def _validate(self, value):
        '''
        >>> IsPositiveValidator('score')._validate(5)
        >>> IsPositiveValidator('score')._validate('aaa')
        'should be int/float'
        >>> IsPositiveValidator('score')._validate(-1)
        'should be positive'
        '''
        error = super(IsPositiveValidator, self)._validate(value)
        if error is not None:
            return error

        if value < 0:
            return 'should be positive'
is_positive = IsPositiveValidator

class NonNegativeValidator(IsNumberValidator):
    def _validate(self, value):
        '''
        >>> NonNegativeValidator('score')._validate(5)
        >>> NonNegativeValidator('score')._validate(0)
        'should be non negative'
        >>> NonNegativeValidator('score')._validate('aaa')
        'should be int/float'
        '''
        error = super(NonNegativeValidator, self)._validate(value)
        if error is not None:
            return error

        if value <= 0:
            return 'should be non negative'
non_negative = NonNegativeValidator

class MaxLengthValidator(OfTypeValidator):
    def __init__(self, param, max_length, error_class=None):
        super(MaxLengthValidator, self).__init__(param, six.string_types, error_class=error_class)
        self._max_length = max_length

    def _validate(self, value):
        '''
        >>> MaxLengthValidator('name', 8)._validate('12345')
        >>> MaxLengthValidator('name', 8)._validate('123456789')
        'should be less than 8 chars'
        >>> MaxLengthValidator('name', 8)._validate(123) is not None
        True
        '''
        error = super(MaxLengthValidator, self)._validate(value)
        if error is not None:
            return error

        if len(value) > self._max_length:
            return 'should be less than %d chars' % self._max_length
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
        'should match regex "[a-z]+"'
        >>> MatchRegexValidator('name', '[a-z]+')._validate(111) is not None
        True
        '''
        error = super(MatchRegexValidator, self)._validate(value)
        if error is not None:
            return error

        if not self._compiled_regex.match(value):
            return 'should match regex "%s"' % self._regex
