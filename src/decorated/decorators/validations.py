# -*- coding: utf-8 -*-
import re
from collections import Iterable
from decimal import Decimal

import six

from decorated.base.function import WrapperFunction
from decorated.util import dutil

_NUMBER_TYPES = list(six.integer_types) + [float, Decimal]
try:
    from cdecimal import Decimal as CDecimal
    _NUMBER_TYPES.append(CDecimal)
except Exception:
    pass
_NUMBER_TYPES = tuple(_NUMBER_TYPES)

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

class BetweenValidator(Validator):
    def __init__(self, param, lower, upper, error_class=None):
        super(BetweenValidator, self).__init__(param, error_class=error_class)
        self._lower = lower
        self._upper = upper

    def _validate(self, value):
        '''
        number value
        >>> BetweenValidator('score', 1, 10)._validate(5)
        >>> BetweenValidator('score', 1, 10)._validate(0)
        'should be between "1" and "10"'
        >>> BetweenValidator('score', 1, 10)._validate(11)
        'should be between "1" and "10"'

        string value
        >>> BetweenValidator('rank', 'A', 'D')._validate('B')
        >>> BetweenValidator('rank', 'A', 'D')._validate('E')
        'should be between "A" and "D"'
        '''
        if value < self._lower or value > self._upper:
            return 'should be between "%s" and "%s"' % (self._lower, self._upper)
between = BetweenValidator

class ChoicesValidator(Validator):
    def __init__(self, param, choices, error_class=None):
        super(ChoicesValidator, self).__init__(param, error_class=error_class)
        self._choices = choices

    def _validate(self, value):
        '''
        >>> ChoicesValidator('id', [1, 2, 3])._validate(2)
        >>> ChoicesValidator('id', [1, 2, 3])._validate(0)
        'should be one of [1, 2, 3]'
        '''
        if value not in self._choices:
            return 'should be one of %s' % self._choices
choices = ChoicesValidator

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
        >>> NotEmptyValidator('values')._validate(True)
        >>> NotEmptyValidator('values')._validate(False)
        >>> NotEmptyValidator('values')._validate(None)
        'should not be empty'
        >>> NotEmptyValidator('values')._validate([])
        'should not be empty'
        >>> NotEmptyValidator('values')._validate('')
        'should not be empty'
        '''
        if not value and not isinstance(value, bool):
            return 'should not be empty'
not_empty = NotEmptyValidator

class TypeValidator(Validator):
    def __init__(self, param, types, error_class=None):
        super(TypeValidator, self).__init__(param, error_class=error_class)
        self._types = types
        if isinstance(types, Iterable):
            self._types_string = '/'.join([t.__name__ for t in types])
        else:
            self._types_string = types.__name__

    def _validate(self, value):
        '''
        >>> TypeValidator('value', int)._validate(111)
        >>> TypeValidator('value', int)._validate('111')
        'should be int'
        >>> TypeValidator('value', (int, float))._validate('111')
        'should be int/float'
        '''
        if not isinstance(value, self._types):
            return 'should be %s' % self._types_string
type = TypeValidator

class NumberValidator(TypeValidator):
    def __init__(self, param, error_class=None):
        super(NumberValidator, self).__init__(param, _NUMBER_TYPES, error_class=error_class)
number = NumberValidator

class PositiveValidator(NumberValidator):
    def _validate(self, value):
        '''
        >>> PositiveValidator('score')._validate(5)
        >>> PositiveValidator('score')._validate(-1)
        'should be positive'
        >>> PositiveValidator('score')._validate('aaa') is None
        False
        '''
        error = super(PositiveValidator, self)._validate(value)
        if error is not None:
            return error

        if value < 0:
            return 'should be positive'
positive = PositiveValidator

class NonNegativeValidator(NumberValidator):
    def _validate(self, value):
        '''
        >>> NonNegativeValidator('score')._validate(5)
        >>> NonNegativeValidator('score')._validate(0)
        'should be non negative'
        >>> NonNegativeValidator('score')._validate('aaa') is None
        False
        '''
        error = super(NonNegativeValidator, self)._validate(value)
        if error is not None:
            return error

        if value <= 0:
            return 'should be non negative'
non_negative = NonNegativeValidator

class MaxLengthValidator(TypeValidator):
    def __init__(self, param, max_length, error_class=None):
        super(MaxLengthValidator, self).__init__(param, six.string_types, error_class=error_class)
        self._max_length = max_length

    def _validate(self, value):
        '''
        >>> MaxLengthValidator('name', 8)._validate('12345')
        >>> MaxLengthValidator('name', 8)._validate('123456789')
        'should be less than 8 chars'
        >>> MaxLengthValidator('name', 8)._validate(123) is None
        False
        '''
        error = super(MaxLengthValidator, self)._validate(value)
        if error is not None:
            return error

        if len(value) > self._max_length:
            return 'should be less than %d chars' % self._max_length
max_length = MaxLengthValidator

class RegexValidator(TypeValidator):
    def __init__(self, param, regex, error_class=None):
        super(RegexValidator, self).__init__(param, six.string_types, error_class=error_class)
        self._regex = regex
        self._compiled_regex = re.compile(regex)

    def _validate(self, value):
        '''
        >>> RegexValidator('name', '[a-z]+')._validate('aaa')
        >>> RegexValidator('name', '[a-z]+')._validate('111')
        'should match regex "[a-z]+"'
        >>> RegexValidator('name', '[a-z]+')._validate(111) is None
        False
        '''
        error = super(RegexValidator, self)._validate(value)
        if error is not None:
            return error

        if not self._compiled_regex.match(value):
            return 'should match regex "%s"' % self._regex
regex = RegexValidator
