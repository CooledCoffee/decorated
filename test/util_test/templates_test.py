# -*- coding: utf-8 -*-
from decorated.util import templates
from decorated.util.templates import StringPart, VariablePart
from unittest.case import TestCase

class CompileTest(TestCase):
    def test_valid_1(self):
        template = templates.compile('Calculating {a} + {b} ...')
        self.assertEqual(5, len(template._parts))
        self.assertIsInstance(template._parts[0], StringPart)
        self.assertEqual('Calculating ', template._parts[0]._expression)
        self.assertIsInstance(template._parts[1], VariablePart)
        self.assertEqual('a', template._parts[1]._expression)
        self.assertIsInstance(template._parts[2], StringPart)
        self.assertEqual(' + ', template._parts[2]._expression)
        self.assertIsInstance(template._parts[3], VariablePart)
        self.assertEqual('b', template._parts[3]._expression)
        self.assertIsInstance(template._parts[4], StringPart)
        self.assertEqual(' ...', template._parts[4]._expression)
        
    def test_valid_2(self):
        template = templates.compile('Calculation succeeded.')
        self.assertEqual(1, len(template._parts))
        self.assertIsInstance(template._parts[0], StringPart)
        self.assertEqual('Calculation succeeded.', template._parts[0]._expression)
        
    def test_valid_3(self):
        template = templates.compile('{a}{b}{c}')
        self.assertEqual(3, len(template._parts))
        self.assertIsInstance(template._parts[0], VariablePart)
        self.assertEqual('a', template._parts[0]._expression)
        self.assertIsInstance(template._parts[1], VariablePart)
        self.assertEqual('b', template._parts[1]._expression)
        self.assertIsInstance(template._parts[2], VariablePart)
        self.assertEqual('c', template._parts[2]._expression)
