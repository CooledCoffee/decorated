# -*- coding: utf-8 -*-
import doctest

class TemplateError(Exception):
    pass

class Template(object):
    def __init__(self, expression, parts):
        self._expression = expression
        self._parts = parts
        
    def eval(self, values):
        parts = []
        for p in self._parts:
            try:
                part = p.eval(values)
                part = str(part)
                parts.append(part)
            except Exception:
                raise TemplateError('Failed to evaluate expression "%s" in template "%s".' % (p._expression, self._expression))
        return ''.join(parts)

class Part(object):
    def __init__(self, expression):
        self._expression = expression
        
class StringPart(Part):
    '''
    >>> StringPart('abc').eval({'a': 1, 'b': 2})
    'abc'
    '''
    def eval(self, variables):
        return self._expression
    
class VariablePart(Part):
    '''
    >>> from decorated.base.dict import Dict
    >>> VariablePart('"abc"').eval({'a': 1, 'b': 2})
    'abc'
    >>> VariablePart('a').eval({'a': 1, 'b': 2})
    1
    >>> VariablePart('user.id').eval({'user': Dict(id=1)})
    1
    >>> VariablePart('user["id"]').eval({'user': {'id': 1}})
    1
    '''
    def eval(self, variables):
        return eval(self._expression, variables)

def compile(template, names):
    parts = []
    expression = ''
    for c in template:
        if c == '{':
            if expression:
                parts.append(StringPart(expression))
                expression = ''
        elif c == '}':
            variable = expression.split('.', 1)[0].split('[', 1)[0]
            if not variable in names:
                raise TemplateError('Unknown variable "%s" in template "%s".' % (expression, template))
            parts.append(VariablePart(expression))
            expression = ''
        else:
            expression += c
    if expression:
        parts.append(StringPart(expression))
    return Template(template, parts)

if __name__ == '__main__':
    doctest.testmod()
    