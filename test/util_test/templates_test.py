# -*- coding: utf-8 -*-
from decorated.base.dict import Dict
from decorated.util import templates
from decorated.util.templates import StringPart, VariablePart, TemplateError
from unittest.case import TestCase

class CompileTest(TestCase):
    def test_normal(self):
        template = templates.compile('Calculating {a} + {b} ...', ['a', 'b', 'c'])
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
        
    def test_pure_string(self):
        template = templates.compile('Calculation succeeded.', ['a', 'b', 'c'])
        self.assertEqual(1, len(template._parts))
        self.assertIsInstance(template._parts[0], StringPart)
        self.assertEqual('Calculation succeeded.', template._parts[0]._expression)
        
    def test_begin_ends_with_vars(self):
        template = templates.compile('{a}{b}{c}', ['a', 'b', 'c'])
        self.assertEqual(3, len(template._parts))
        self.assertIsInstance(template._parts[0], VariablePart)
        self.assertEqual('a', template._parts[0]._expression)
        self.assertIsInstance(template._parts[1], VariablePart)
        self.assertEqual('b', template._parts[1]._expression)
        self.assertIsInstance(template._parts[2], VariablePart)
        self.assertEqual('c', template._parts[2]._expression)
        
    def test_attr(self):
        template = templates.compile('{user.id}', ['user'])
        self.assertEqual('user.id', template._parts[0]._expression)
        
    def test_item(self):
        template = templates.compile('{user["id"]}', ['user'])
        self.assertEqual('user["id"]', template._parts[0]._expression)
        
    def test_missing_var(self):
        with self.assertRaises(TemplateError):
            templates.compile('{d}', ['a', 'b', 'c'])
    
class EvalTest(TestCase):
    def test_succeed(self):
        template = templates.compile('Calculating {a} + {b} ...', ['a', 'b', 'c'])
        result = template.eval({'a': 1, 'b': 2, 'c': 3})
        self.assertEqual('Calculating 1 + 2 ...', result)
        
    def test_attr_not_found(self):
        template = templates.compile('{user.name}', ['user'])
        with self.assertRaises(TemplateError):
            template.eval({'user': Dict(id=1)})
            
    def test_item_not_found(self):
        template = templates.compile('{user["name"]}', ['user'])
        with self.assertRaises(TemplateError):
            template.eval({'user': {'id': 1}})
            