# -*- coding: utf-8 -*-
import re

import six

from decorated.decorators.validations.validators.misc import TypeValidator


class StringValidator(TypeValidator):
    def __init__(self, param, error_class=None):
        super(StringValidator, self).__init__(param, six.string_types, error_class=error_class)
        
class MaxLengthValidator(StringValidator):
    def __init__(self, param, max_length, error_class=None):
        super(MaxLengthValidator, self).__init__(param, error_class=error_class)
        self._max_length = max_length

    def _validate(self, value):
        '''
        >>> MaxLengthValidator('name', 8)._validate('12345')
        >>> MaxLengthValidator('name', 8)._validate('123456789')
        'should be less than 8 chars'
        '''
        if len(value) > self._max_length:
            return 'should be less than %d chars' % self._max_length

class RegexValidator(StringValidator):
    def __init__(self, param, regex, error_class=None):
        super(RegexValidator, self).__init__(param, error_class=error_class)
        self._regex = regex
        self._compiled_regex = re.compile(regex)

    def _validate(self, value):
        '''
        >>> RegexValidator('name', '[a-z]+')._validate('aaa')
        >>> RegexValidator('name', '[a-z]+')._validate('111')
        'should match regex "[a-z]+"'
        '''
        if not self._compiled_regex.match(value):
            return 'should match regex "%s"' % self._regex
        