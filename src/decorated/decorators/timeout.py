# -*- coding: utf-8 -*-
from decorated.base.function import ContextFunction
import signal
import time

ENABLED = True

class Timeout(ContextFunction):
    def _init(self, seconds):
        self._seconds = seconds
        self._old_handler = None
        self._old_alarm_time = None
        
    def _before(self):
        if not ENABLED or self._seconds == 0:
            return
        
        self._old_handler = signal.getsignal(signal.SIGALRM)
        def _timeout(*args):
            raise TimeoutError()
        signal.signal(signal.SIGALRM, _timeout)
        old_alarm = signal.alarm(self._seconds)
        if old_alarm != 0:
            self._old_alarm_time = time.time() + old_alarm
    
    def _after(self, ret, error):
        if not ENABLED or self._seconds == 0:
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
    
class TimeoutError(Exception):
    pass
