# -*- coding: utf-8 -*-
from decorated.decorators.conditional import Conditional
from decorated.testing import DecoratedFixture
from fixtures2 import TestCase

class DisableTest(TestCase):
    def test(self):
        # set up
        fixture = self.useFixture(DecoratedFixture())
        fixture.disable(Conditional)
        @Conditional('a != 0')
        def foo(a):
            return a
        
        # test
        self.assertEqual(0, foo(0))
        self.assertEqual(1, foo(1))
        