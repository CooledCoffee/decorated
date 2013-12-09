# -*- coding: utf-8 -*-
from decorated.function import Function, BoundedFunction, PartialFunction
from decorated.util.conditional import conditional
from decorated.util.retries import retries

Function = Function
PartialFunction = PartialFunction
BoundedFunction = BoundedFunction

retries = retries
conditional = conditional
