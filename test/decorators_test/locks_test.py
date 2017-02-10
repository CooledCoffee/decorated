# -*- coding: utf-8 -*-
import time
from threading import Thread
from unittest.case import TestCase

from decorated.decorators.locks import MemoryLock


class MemoryLockTest(TestCase):
    def test_simple(self):
        lock = MemoryLock()
        @lock
        def foo(a):
            return a
        result = foo(1)
        self.assertEqual(1, result)
        
    def test_normal(self):
        # set up
        lock = MemoryLock()
        @lock
        def foo():
            time.sleep(0.01)
                
        # test
        thread1 = Thread(target=foo)
        thread2 = Thread(target=foo)
        begin = time.time()
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        end = time.time()
        self.assertGreater(end - begin, 0.02)
        
    def test_error(self):
        lock = MemoryLock()
        @lock
        def foo():
            raise Exception
        with self.assertRaises(Exception):
            foo()

class FileLockTest(TestCase):
    def test_simple(self):
        lock = MemoryLock()

        @lock
        def foo(a):
            return a

        result = foo(1)
        self.assertEqual(1, result)

    def test_normal(self):
        # set up
        lock = MemoryLock()

        @lock
        def foo():
            time.sleep(0.01)

        # test
        thread1 = Thread(target=foo)
        thread2 = Thread(target=foo)
        begin = time.time()
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        end = time.time()
        self.assertGreater(end - begin, 0.02)

    def test_error(self):
        lock = MemoryLock()

        @lock
        def foo():
            raise Exception

        with self.assertRaises(Exception):
            foo()
