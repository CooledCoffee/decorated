# -*- coding: utf-8 -*-
import six

from decorated.base.expression import Expression
from decorated.decorators.validations import TypeValidator, MaxLengthValidator
from decorated.decorators.validations.engine import ValidationEngine
from decorated.decorators.validations.errors import ValidationError
from decorated.decorators.validations.validators.base import Validator
from testutil import TestCase


class EvalValueTest(TestCase):
    def test_basic(self):
        validator = Validator('key')
        result = validator._eval_value({'key': 'aaa'}, ValidationError)
        self.assertEqual('aaa', result)
        
    def test_not_found(self):
        validator = Validator('key')
        with self.assertRaises(ValidationError):
            validator._eval_value({}, ValidationError)
            
    def test_expression(self):
        validator = Validator(Expression('key.upper()'))
        result = validator._eval_value({'key': 'aaa'}, ValidationError)
        self.assertEqual('AAA', result)
        
    def test_bad_expression(self):
        validator = Validator(Expression('key.upper()'))
        with self.assertRaises(ValidationError):
            validator._eval_value({'key': 1}, ValidationError)
        
class ValidateTest(TestCase):
    def test_pass(self):
        class TestValidator(Validator):
            def _validate(self, value):
                return None
        validator = TestValidator('id', error_class=ValidationError)
        validator.validate({'id': None, 'name': 'aaa'})
        
    def test_failed(self):
        class TestValidator(Validator):
            def _validate(self, value):
                return 'is required'
        validator = TestValidator('id', error_class=ValidationError)
        with self.assertRaises(ValidationError):
            validator.validate({'id': None, 'name': 'aaa'})
        
class ValidationEngineTest(TestCase):
    def test_single_validator(self):
        # set up
        engine = ValidationEngine()
        @engine.rules(TypeValidator('id', six.string_types))
        def foo(id):
            pass

        # test success
        foo('111')

        # test error
        with self.assertRaises(ValidationError):
            foo(111)

    def test_multi_validators(self):
        # set up
        engine = ValidationEngine()
        @engine.rules([
            TypeValidator('id', six.string_types),
            MaxLengthValidator('id', 4),
        ])
        def foo(id):
            pass

        # test success
        foo('111')

        # test error
        with self.assertRaises(ValidationError):
            foo('11111')
