#!/usr/bin/python
from decorated.decorators.validations.engine import ValidationEngine
from decorated.decorators.validations.validators.misc import ChoicesValidator, NotEmptyValidator, NotNoneValidator, \
    TypeValidator
from decorated.decorators.validations.validators.number import BetweenValidator, NonNegativeValidator, NumberValidator, \
    PositiveValidator, GeValidator, GtValidator, LeValidator, LtValidator
from decorated.decorators.validations.validators.string import MaxLengthValidator, RegexValidator

engine = ValidationEngine()

between = BetweenValidator
choices = ChoicesValidator
ge = GeValidator
gt = GtValidator
le = LeValidator
lt = LtValidator
max_length = MaxLengthValidator
not_empty = NotEmptyValidator
not_none = NotNoneValidator
non_negative = NonNegativeValidator
number = NumberValidator
positive = PositiveValidator
regex = RegexValidator
type = TypeValidator
