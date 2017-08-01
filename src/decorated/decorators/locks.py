# -*- coding: utf-8 -*-
import fcntl
import os
from threading import RLock

from decorated import ContextFunction, WrapperFunction


class Lock(ContextFunction):
    def lock(self):
        raise NotImplementedError()

    def unlock(self):
        raise NotImplementedError()

    def _after(self, ret, *args, **kw):
        self.unlock()

    def _before(self, *args, **kw):
        self.lock()

    def _decorate(self, func):
        return _LockProxy(self)(func)

    def _error(self, error, *args, **kw):
        self.unlock()

class FileLock(Lock):
    def _init(self, path): # pylint: disable=arguments-differ
        super(FileLock, self)._init()
        self._path = path
        self._fd = None

    def lock(self):
        _create_file_if_not_exist(self._path)
        self._fd = os.open(self._path, os.O_RDWR)
        fcntl.flock(self._fd, fcntl.LOCK_EX)

    def unlock(self):
        fcntl.flock(self._fd, fcntl.LOCK_UN)

class MemoryLock(Lock):
    def _init(self, *args, **kw):
        super(MemoryLock, self)._init(*args, **kw)
        self._lock = RLock()

    def lock(self):
        self._lock.acquire()

    def unlock(self):
        self._lock.release()

class _LockProxy(WrapperFunction):
    def _after(self, ret, *args, **kw):
        self._target.unlock()

    def _before(self, *args, **kw):
        self._target.lock()

    def _error(self, error, *args, **kw):
        self._target.unlock()

    def _init(self, target): # pylint: disable=arguments-differ
        super(_LockProxy, self)._init()
        self._target = target

    def _is_init_args(self, *args, **kw):
        return True

def _create_file_if_not_exist(path):
    try:
        f = open(path, 'w')
        f.close()
    except OSError:
        pass
