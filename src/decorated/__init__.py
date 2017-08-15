# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
from decorated.base.false import NOTSET
from decorated.base.context import Context, ctx
from decorated.base.function import ContextFunction, Function, WrapperFunction, partial
from decorated.decorators.conditional import Conditional
from decorated.decorators.events import Event, event
from decorated.decorators.files import TempDir, TempFile, WritingFile
from decorated.decorators.once import Once, OnceSession
from decorated.decorators.profile import Profile
from decorated.decorators.remove_extra_args import RemoveExtraArgs
from decorated.decorators.retries import Retries
from decorated.decorators.timeit import TimeIt
from decorated.decorators.timeout import Timeout

conditional = Conditional
once = Once
OnceSession = OnceSession
profile = Profile
remove_extra_args = RemoveExtraArgs
retries = Retries
tempfile = TempFile
tempdir = TempDir
timeit = TimeIt
timeout = Timeout
writing_file = WritingFile
