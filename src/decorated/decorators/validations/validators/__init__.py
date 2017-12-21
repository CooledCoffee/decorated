# -*- coding: utf-8 -*-
from decorated.decorators.validations.engine import ValidationEngine
from decorated.decorators.validations.validators.misc import ChoicesValidator, NotEmptyValidator, NotNoneValidator, \
    TypeValidator
from decorated.decorators.validations.validators.number import BetweenValidator, NonNegativeValidator, NumberValidator, \
    PositiveValidator
from decorated.decorators.validations.validators.string import MaxLengthValidator, RegexValidator

engine = ValidationEngine()

between = BetweenValidator
choices = ChoicesValidator
max_length = MaxLengthValidator
not_empty = NotEmptyValidator
not_none = NotNoneValidator
non_negative = NonNegativeValidator
number = NumberValidator
positive = PositiveValidator
regex = RegexValidator
type = TypeValidator
