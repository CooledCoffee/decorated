# -*- coding: utf-8 -*-
from decorated.base.function import Function
from threading import RLock
import os

class Synchronized(Function):
    def _init(self, lock):
        self._lock = lock
        
    def _call(self, *args, **kw):
        with self._lock:
            return super(Synchronized, self)._call(*args, **kw)

MemoryLock = RLock

class FileLock(object):
    def __init__(self, path):
        self._path = path
        
    def __enter__(self):
        import fcntl
        _create_file_if_not_exist(self._path)
        self._fd = os.open(self._path, os.O_RDWR)
        fcntl.flock(self._fd, fcntl.LOCK_EX)
        return self
    
    def __exit__(self, t, v, tb):
        import fcntl
        fcntl.flock(self._fd, fcntl.LOCK_UN)
    
def _create_file_if_not_exist(path):
    try:
        f = open(path, 'w')
        f.close()
    except OSError:
        pass
    