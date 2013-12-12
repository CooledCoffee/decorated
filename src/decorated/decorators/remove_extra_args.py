# -*- coding: utf-8 -*-
from decorated.base.function import Function

class RemoveExtraArgs(Function):
    def _call(self, *args, **kw):
        kw = self._resolve_args(*args, **kw)
        return super(RemoveExtraArgs, self)._call(**kw)
    