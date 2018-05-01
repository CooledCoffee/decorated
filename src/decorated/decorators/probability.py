# -*- coding: utf-8 -*-
import random

from decorated.base.function import Function


class Probability(Function):
    def _call(self, *args, **kw):
        if random.random() < self._p:
            return super(Probability, self)._call(*args, **kw)
        else:
            return None
        
    def _init(self, p):
        self._p = p
