# -*- coding: utf-8 -*-
from decorated.base.expression import Expression, ExpressionError
from testutil import TestCase


class ExpressionTest(TestCase):
    def test_success(self):
        expression = Expression('a + b')
        result = expression({'a': 1, 'b': 2})
        self.assertEqual(3, result)
        
    def test_failed(self):
        expression = Expression('a + c')
        with self.assertRaises(ExpressionError):
            expression({'a': 1, 'b': 2})
            
    def test_no_access_to_builtins(self):
        expression = Expression('map')
        with self.assertRaises(ExpressionError):
            expression({})
            
    def test_bad_syntax(self):
        with self.assertRaises(ExpressionError):
            Expression('!@#$%')
            