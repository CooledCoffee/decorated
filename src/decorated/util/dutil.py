# -*- coding: utf-8 -*-
from collections import Iterable

import six

_SAFE_BUILTINS = {
    '__builtins__': None,
    'Exception': Exception,
    'False': False,
    'None': None,
    'True': True,
    'float': float,
    'int': int,
    'isinstance': isinstance,
    'issubclass': issubclass,
    'list': list,
    'len': len,
    'max': max,
    'min': min,
    'round': round,
    'sorted': sorted,
    'str': str,
    'sum': sum,
    'tuple': tuple,
    'type': type,
}
if six.PY2:
    _SAFE_BUILTINS['unicode'] = unicode

def generate_safe_context(variables):
    ctx = dict(_SAFE_BUILTINS)
    ctx.update(variables)
    return ctx

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
