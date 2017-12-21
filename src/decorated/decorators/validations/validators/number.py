# -*- coding: utf-8 -*-
from decimal import Decimal

import six

from decorated.decorators.validations.validators.misc import TypeValidator

_NUMBER_TYPES = list(six.integer_types) + [float, Decimal]
try:
    from cdecimal import Decimal as CDecimal
    _NUMBER_TYPES.append(CDecimal)
except Exception:
    pass
_NUMBER_TYPES = tuple(_NUMBER_TYPES)

class NumberValidator(TypeValidator):
    def __init__(self, param, error_class=None):
        super(NumberValidator, self).__init__(param, _NUMBER_TYPES, error_class=error_class)

class BetweenValidator(NumberValidator):
    def __init__(self, param, lower, upper, error_class=None):
        super(BetweenValidator, self).__init__(param, error_class=error_class)
        self._lower = lower
        self._upper = upper

    def _validate(self, value):
        '''
        >>> BetweenValidator('score', 1, 10)._validate(5)
        >>> BetweenValidator('score', 1, 10)._validate(0)
        'should be between "1" and "10"'
        >>> BetweenValidator('score', 1, 10)._validate(11)
        'should be between "1" and "10"'
        '''
        if value < self._lower or value > self._upper:
            return 'should be between "%s" and "%s"' % (self._lower, self._upper)

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
        