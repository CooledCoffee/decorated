# -*- coding: utf-8 -*-
from fixtures2 import PatchesFixture

class DecoratedFixture(PatchesFixture):
    def disable(self, cls):
        path = '.'.join([cls.__module__, cls.__name__, '_call'])
        def _call(self, *args, **kw):
            return self._func(*args, **kw)
        self.patch(path, _call)
    