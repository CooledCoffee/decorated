# -*- coding: utf-8 -*-
from decorated.decorators.probability import Probability
from testutil import DecoratedTest


class ProbabilityTest(DecoratedTest):
    def test(self):
        @Probability(0.5)
        def add(a, b):
            return a + b
        result = add(1, 2)
        self.assertIn(result, [3, None])
