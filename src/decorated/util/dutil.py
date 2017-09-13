# -*- coding: utf-8 -*-
from collections import Iterable

import six


def listify(value_or_values):
    '''
    >>> listify(['aaa', 'bbb'])
    ['aaa', 'bbb']
    >>> listify(('aaa', 'bbb'))
    ['aaa', 'bbb']
    >>> listify('aaa')
    ['aaa']
    '''
    if isinstance(value_or_values, list):
        return value_or_values
    elif isinstance(value_or_values, six.string_types):
        return [value_or_values]
    elif isinstance(value_or_values, Iterable):
        return list(value_or_values)
    else:
        return [value_or_values]
