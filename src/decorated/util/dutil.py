# -*- coding: utf-8 -*-
from collections import Iterable


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
    elif isinstance(value_or_values, basestring):
        return [value_or_values]
    elif isinstance(value_or_values, Iterable):
        return list(value_or_values)
    else:
        return [value_or_values]
