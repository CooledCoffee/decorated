# -*- coding: utf-8 -*-
from collections import Iterable

from decorated.decorators.validations.validators.base import Validator


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

class NotNoneValidator(Validator):
    def _validate(self, value):
        '''
        >>> NotNoneValidator('id')._validate(111)
        >>> NotNoneValidator('id')._validate(None)
        'should not be none'
        '''
        if value is None:
            return 'should not be none'

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
        