# -*- coding: utf-8 -*-
from decorated.decorators.remove_extra_args import RemoveExtraArgs
from unittest.case import TestCase

@RemoveExtraArgs
def foo(a, b):
    return a

class RemoveExtraArgsTest(TestCase):
    def test_normal(self):
        self.assertEqual(1, foo(1, 2))
        
    def test_extra_kw(self):
        self.assertEqual(1, foo(1, 2, timestamp=123))
        self.assertEqual(1, foo(1, b=2, timestamp=123))
        self.assertEqual(1, foo(a=1, b=2, timestamp=123))
        