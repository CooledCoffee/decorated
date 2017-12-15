# -*- coding: utf-8 -*-
from decorated.util import dutil


class Expression(object):
    def __init__(self, string):
        self._string = string
        try:
            self._expression = compile(string, '<string>', 'eval')
        except SyntaxError:
            raise ExpressionError('Bad expression "%s".' % string)
        
    def __call__(self, **variables):
        variables = dutil.generate_safe_context(variables)
        try:
            return eval(self._expression, variables)
        except Exception as e:
            raise ExpressionError('Failed to evaluate expression "%s". Error was: %s' % (self._string, e))
        
    def __str__(self):
        return self._string

class ExpressionError(Exception):
    pass
