# -*- coding: utf-8 -*-
from decorated.base.function import Function
from fixtures2 import PatchesFixture

class DecoratedFixture(PatchesFixture):
    def disable(self, cls):
        def _call(self, *args, **kw):
            if self._func is None:
                return self._decorate(args[0])
            else:
                return self._func(*args, **kw)
        self.patch_object(cls, '_old__call__', cls.__call__)
        self.patch_object(cls, '__call__', Function._call)
    
    def enable(self, cls):
        cls.__call__ = cls._old__call__