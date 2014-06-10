# -*- coding: utf-8 -*-
from decorated.decorators.timeout import Timeout, TimeoutError
from fixtures._fixtures.monkeypatch import MonkeyPatch
from fixtures2 import TestCase
import signal
import time

class TimeoutTest(TestCase):
    def test_within_timeout(self):
        with Timeout(10):
            pass
        self.assertEquals(signal.SIG_DFL, signal.getsignal(signal.SIGALRM))
        
    def test_exceed_timeout(self):
        with self.assertRaises(TimeoutError):
            with Timeout(1):
                time.sleep(10)
        self.assertEquals(signal.SIG_DFL, signal.getsignal(signal.SIGALRM))
        
    def test_no_timeout(self):
        with Timeout(0):
            time.sleep(0.01)
        self.assertEquals(signal.SIG_DFL, signal.getsignal(signal.SIGALRM))
            
    def test_multi_alarms(self):
        with self.assertRaises(TimeoutError):
            with Timeout(3):
                with self.assertRaises(TimeoutError):
                    with Timeout(1):
                        time.sleep(10)
                time.sleep(10)
        self.assertEquals(signal.SIG_DFL, signal.getsignal(signal.SIGALRM))
        
    def test_outer_alarm_overdue(self):
        with self.assertRaises(TimeoutError):
            with Timeout(1):
                with self.assertRaises(TimeoutError):
                    with Timeout(2):
                        time.sleep(10)
                time.sleep(10)
        self.assertEquals(signal.SIG_DFL, signal.getsignal(signal.SIGALRM))
        
    def test_disabled(self):
        self.useFixture(MonkeyPatch('decorated.decorators.timeout.ENABLED', False))
        with Timeout(1):
            time.sleep(2)
            