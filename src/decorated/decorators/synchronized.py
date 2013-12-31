# -*- coding: utf-8 -*-
from decorated.base.function import Function
from threading import RLock

class Synchronized(Function):
    def _init(self, lock):
        self._lock = lock
        
    def _call(self, *args, **kw):
        with self._lock:
            return super(Synchronized, self)._call(*args, **kw)

MemoryLock = RLock
