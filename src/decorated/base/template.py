# -*- coding: utf-8 -*-
import re

from decorated.util import dutil


class Template(object):
    def __init__(self, string):
        self._string = string
        source = _generate_source(string)
        self._code = compile(source, '<string>', 'exec')
        
    def __call__(self, **variables):
        variables = dutil.generate_safe_context(variables)
        exec(self._code, variables)
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
    parts.append(str(%s))
except Exception:
    parts.append('{error:%s}')
''' % (part, part)
            parts[i] = part.strip()
        else:
            parts[i] = "parts.append('%s')" % part
    parts = '\n'.join([p for p in parts if p is not None])
    source = '''
parts = []
%s
result = ''.join(parts)
''' % parts
    return source.strip()
