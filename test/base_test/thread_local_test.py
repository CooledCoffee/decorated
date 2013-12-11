# -*- coding: utf-8 -*-
from decorated.base.thread_local import ThreadLocal
from threading import Thread
from unittest.case import TestCase

class ThreadLocalTest(TestCase):
    def test_local_thread(self):
        local = ThreadLocal(0)
        self.assertEquals(0, local.get())
        local.set(1)
        self.assertEquals(1, local.get())
        local.reset()
        self.assertEquals(0, local.get())
        
    def test_another_thread(self):
        local = ThreadLocal(0)
        values = []
        class AnotherThread(Thread):
            def run(self):
                values.append(local.get())
                local.set(1)
                values.append(local.get())
                local.reset()
                values.append(local.get())
        thread = AnotherThread()
        thread.start()
        thread.join()
        self.assertEquals([0, 1, 0], values)
        