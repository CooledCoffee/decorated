# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import signal

class TimeoutError(Exception):
    pass

class Timeout(object):
    def __init__(self, seconds):
        self._seconds = seconds
        self._old_handler = None
        self._old_alarm_time = None
        
    def __enter__(self):
        if self._seconds != 0:
            self._old_handler = signal.getsignal(signal.SIGALRM)
            def _timeout(*args):
                raise TimeoutError()
            signal.signal(signal.SIGALRM, _timeout)
            old_alarm = signal.alarm(self._seconds)
            if old_alarm != 0:
                self._old_alarm_time = datetime.now() + timedelta(seconds=old_alarm)
        return self
    
    def __exit__(self, *args):
        signal.alarm(0)
        if self._old_handler is not None:
            signal.signal(signal.SIGALRM, self._old_handler)
        if self._old_alarm_time is not None:
            remain_time = self._old_alarm_time - datetime.now()
            remain_seconds = int(remain_time.total_seconds())
            if remain_seconds < 1:
                # old alarm is overdue
                # the best we can do is rescheduling it at 1 second later
                remain_seconds = 1
            signal.alarm(remain_seconds)
    