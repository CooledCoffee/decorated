#!/usr/bin/python
from decorated.decorators.validations.engine import ValidationEngine
from decorated.decorators.validations.errors import ValidationError
from decorated.decorators.validations.validators.misc import ChoicesValidator, FalseValidator, NotEmptyValidator, \
    NotNoneValidator, TrueValidator, TypeValidator
from decorated.decorators.validations.validators.number import BetweenValidator, GeValidator, GtValidator, LeValidator, \
    LtValidator, NonNegativeValidator, NumberValidator, PositiveValidator
from decorated.decorators.validations.validators.string import MaxLengthValidator, RegexValidator

engine = ValidationEngine()

between = BetweenValidator
choices = ChoicesValidator
false = FalseValidator
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
true = TrueValidator
type = TypeValidator
