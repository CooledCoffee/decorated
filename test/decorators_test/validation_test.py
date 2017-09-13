# -*- coding: utf-8 -*-
import six

from decorated.decorators import validation
from decorated.decorators.validation import ValidationEngine, ValidationError
from testutil import TestCase


class ValidationEngineTest(TestCase):
    def test_single_validator(self):
        # set up
        engine = ValidationEngine()
        @engine.rules(validation.of_type('id', six.string_types))
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
            validation.of_type('id', six.string_types),
            validation.max_length('id', 4),
        ])
        def foo(id):
            pass

        # test success
        foo('111')

        # test error
        with self.assertRaises(ValidationError):
            foo('11111')
