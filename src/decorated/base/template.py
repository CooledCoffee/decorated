# -*- coding: utf-8 -*-
import re

import six

from decorated.util import dutil

if six.PY2:
    _DEFAULT_STRING_TYPE = 'unicode'
else:
    _DEFAULT_STRING_TYPE = 'str'
    
class Template(object):
    def __init__(self, string):
        self._string = string
        source = _generate_source(string)
        self._code = compile(source, '<string>', 'exec')
        
    def __call__(_template_self, **variables): # variables may contain a "self" key
        variables = dutil.generate_safe_context(variables)
        exec(_template_self._code, variables)
        return variables['result']
    
    def __str__(self):
        return self._string

def _generate_source(string):
    parts = re.split('(\{.+?\})', string)
    for i, part in enumerate(parts):
        if part == '':
            parts[i] = None
        elif part.startswith('{') and part.endswith('}'):
            part = part[1:-1]
            part = '''
try:
    parts.append(%s(%s))
except Exception:
    parts.append(u'{error:%s}')
''' % (_DEFAULT_STRING_TYPE, part, part)
            parts[i] = part.strip()
        else:
            parts[i] = "parts.append(u'%s')" % part.replace('\n', '\\n').replace("'", "\\'")
    parts = '\n'.join([p for p in parts if p is not None])
    source = '''
parts = []
%s
result = ''.join(parts)
''' % parts
    return source.strip()
