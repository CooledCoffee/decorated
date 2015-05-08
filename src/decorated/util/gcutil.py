# -*- coding: utf-8 -*-
import gc

class DisableGc(object):
    def __enter__(self):
        self._enabled = gc.isenabled()
        gc.disable()
        
    def __exit__(self, *args, **kw):
        if self._enabled:
            gc.enable()
            