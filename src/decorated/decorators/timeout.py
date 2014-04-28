# -*- coding: utf-8 -*-
from decorated.base.function import Function
import signal
import time

ENABLED = True

class TimeoutError(Exception):
    pass

class Timeout(object):
    def __init__(self, seconds):
        self._seconds = seconds
        self._old_handler = None
        self._old_alarm_time = None
        
    def __enter__(self):
        if ENABLED and self._seconds != 0:
            self._old_handler = signal.getsignal(signal.SIGALRM)
            def _timeout(*args):
                raise TimeoutError()
            signal.signal(signal.SIGALRM, _timeout)
            old_alarm = signal.alarm(self._seconds)
            if old_alarm != 0:
                self._old_alarm_time = time.time() + old_alarm
        return self
    
    def __exit__(self, *args):
        if not ENABLED:
            return
        
        signal.alarm(0)
        if self._old_handler is not None:
            signal.signal(signal.SIGALRM, self._old_handler)
        if self._old_alarm_time is not None:
            remain_seconds = int(self._old_alarm_time - time.time())
            if remain_seconds < 1:
                # old alarm is overdue
                # the best we can do is rescheduling it at 1 second later
                remain_seconds = 1
            signal.alarm(remain_seconds)
    
class TimeoutDecorator(Function):
    def _init(self, seconds):
        super(TimeoutDecorator, self)._init()
        self._seconds = seconds
        
    def _call(self, *args, **kw):
        with Timeout(self._seconds):
            return super(TimeoutDecorator, self)._call(*args, **kw)
