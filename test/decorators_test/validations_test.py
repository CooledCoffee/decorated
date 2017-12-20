# -*- coding: utf-8 -*-
import six

from decorated.decorators import validations
from decorated.decorators.validations import ValidationEngine, ValidationError, Validator
from testutil import TestCase


class ValidateTest(TestCase):
    def test_valid(self):
        class TestValidator(Validator):
            def _validate(self, value):
                return 'is required'
        validator = TestValidator('id', error_class=ValidationError)
        with self.assertRaises(ValidationError) as raises:
            validator.validate({'id': None, 'name': 'aaa'})
        self.assertEqual('Arg "id" is required, got "None" (type=NoneType).', str(raises.exception))
        
class ValidationEngineTest(TestCase):
    def test_single_validator(self):
        # set up
        engine = ValidationEngine()
        @engine.rules(validations.of_type('id', six.string_types))
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
            validations.of_type('id', six.string_types),
            validations.max_length('id', 4),
        ])
        def foo(id):
            pass

        # test success
        foo('111')

        # test error
        with self.assertRaises(ValidationError):
            foo('11111')
