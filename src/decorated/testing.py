# -*- coding: utf-8 -*-
from fixtures2 import PatchesFixture


class DecoratedFixture(PatchesFixture):
    def disable(self, cls):
        cls.enabled = False
    
    def enable(self, cls):
        cls.enabled = True
