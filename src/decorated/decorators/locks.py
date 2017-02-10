# -*- coding: utf-8 -*-
import os
from threading import RLock

import fcntl

from decorated import WrapperFunction


class Lock(WrapperFunction):
    def lock(self):
        raise NotImplementedError()

    def unlock(self):
        raise NotImplementedError()

    def _after(self, ret, *args, **kw):
        self.unlock()

    def _before(self, *args, **kw):
        self.lock()

    def _error(self, error, *args, **kw):
        self.unlock()

class FileLock(Lock):
    def _init(self, path):
        super(FileLock, self)._init()
        self._path = path

    def lock(self):
        _create_file_if_not_exist(self._path)
        self._fd = os.open(self._path, os.O_RDWR)
        fcntl.flock(self._fd, fcntl.LOCK_EX)

    def unlock(self):
        fcntl.flock(self._fd, fcntl.LOCK_UN)

class MemoryLock(Lock):
    def _init(self):
        super(MemoryLock, self)._init()
        self._lock = RLock()

    def lock(self):
        self._lock.acquire()

    def unlock(self):
        self._lock.release()

def _create_file_if_not_exist(path):
    try:
        f = open(path, 'w')
        f.close()
    except OSError:
        pass
