# -*- coding: utf-8 -*-
from decorated.base.context import Context, ctx
from decorated.base.function import Function, partial, WrapperFunction, \
    ContextFunction
from decorated.decorators.conditional import Conditional
from decorated.decorators.events import Event
from decorated.decorators.instantiate import Instantiate
from decorated.decorators.once import Once, OnceSession
from decorated.decorators.remove_extra_args import RemoveExtraArgs
from decorated.decorators.retries import Retries
from decorated.decorators.synchronized import Synchronized
from decorated.decorators.tempfile import TempFile, TempDir
from decorated.decorators.timeout import Timeout

Contxt = Context
ctx = ctx

Function = Function
WrapperFunction = WrapperFunction
ContextFunction = ContextFunction
partial = partial

Event = Event
conditional = Conditional
instantiate = Instantiate
once = Once
OnceSession = OnceSession
remove_extra_args = RemoveExtraArgs
retries = Retries
synchronized = Synchronized
tempfile = TempFile = TempFile
tempdir = TempDir = TempDir
timeout = Timeout = Timeout
