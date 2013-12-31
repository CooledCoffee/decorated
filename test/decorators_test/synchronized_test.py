# -*- coding: utf-8 -*-
from decorated.decorators.synchronized import MemoryLock, Synchronized
from threading import Thread
from unittest.case import TestCase
import time

class SynchronizedTest(TestCase):
    def test_simple(self):
        lock = MemoryLock()
        @Synchronized(lock)
        def foo(a):
            return a
        result = foo(1)
        self.assertEqual(1, result)
        
    def test_normal(self):
        # set up
        lock = MemoryLock()
        @Synchronized(lock)
        def foo():
            time.sleep(0.01)
        class BlockThread(Thread):
            def run(self):
                foo()
                
        # test
        thread1 = BlockThread()
        thread2 = BlockThread()
        begin = time.time()
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        end = time.time()
        self.assertGreater(end - begin, 0.02)
        
    def test_error(self):
        lock = MemoryLock()
        @Synchronized(lock)
        def foo():
            raise Exception
        with self.assertRaises(Exception):
            foo()
        