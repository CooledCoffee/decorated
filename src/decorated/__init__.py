# -*- coding: utf-8 -*-
from decorated.base import NOTSET
from decorated.base.context import Context, ctx
from decorated.base.function import Function, partial, WrapperFunction, \
    ContextFunction
from decorated.decorators import events
from decorated.decorators.conditional import Conditional
from decorated.decorators.events import Event
from decorated.decorators.files import TempFile, TempDir, WritingFile
from decorated.decorators.instantiate import Instantiate
from decorated.decorators.once import Once, OnceSession
from decorated.decorators.profile import Profile
from decorated.decorators.remove_extra_args import RemoveExtraArgs
from decorated.decorators.retries import Retries
from decorated.decorators.synchronized import Synchronized
from decorated.decorators.timeit import TimeIt
from decorated.decorators.timeout import Timeout

NOTSET = NOTSET

Contxt = Context
ctx = ctx

Function = Function
WrapperFunction = WrapperFunction
ContextFunction = ContextFunction
partial = partial

conditional = Conditional
event = events.event
Event = Event
instantiate = Instantiate
once = Once
OnceSession = OnceSession
profile = Profile
remove_extra_args = RemoveExtraArgs
retries = Retries
synchronized = Synchronized
tempfile = TempFile
tempdir = TempDir
timeit = TimeIt
timeout = Timeout
writing_file = WritingFile
