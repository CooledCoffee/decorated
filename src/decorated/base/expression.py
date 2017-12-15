# -*- coding: utf-8 -*-

class Expression(object):
    def __init__(self, expression):
        self._raw_expression = expression
        try:
            self._expression = compile(expression, '<string>', 'eval')
        except SyntaxError:
            raise ExpressionError('Bad expression "%s".' % expression)
        
    def __call__(self, **variables):
        variables = dict(variables, __builtins__=None)
        try:
            return eval(self._expression, variables)
        except Exception as e:
            raise ExpressionError('Failed to evaluate expression "%s". Error was: %s' % (self._raw_expression, e))

class ExpressionError(Exception):
    pass
