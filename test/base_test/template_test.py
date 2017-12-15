# -*- coding: utf-8 -*-
from decorated.base import template
from decorated.base.template import Template
from testutil import TestCase

class GenerateSourceTest(TestCase):
    def test_single_string(self):
        source = template._generate_source('aaa')
        self.assertMultiLineEqual('''
parts = []
parts.append('aaa')
result = ''.join(parts)
'''.strip(), source)
    
    def test_single_variable(self):
        source = template._generate_source('{a}')
        self.assertMultiLineEqual('''
parts = []
try:
    parts.append(str(a))
except Exception:
    parts.append('{error:a}')
result = ''.join(parts)
'''.strip(), source)
    
    def test_multi_variables(self):
        source = template._generate_source('{a}{b}')
        self.assertMultiLineEqual('''
parts = []
try:
    parts.append(str(a))
except Exception:
    parts.append('{error:a}')
try:
    parts.append(str(b))
except Exception:
    parts.append('{error:b}')
result = ''.join(parts)
'''.strip(), source)
    
    def test_strings_and_variables(self):
        source = template._generate_source('aaa {a} bbb {b} ccc')
        self.assertMultiLineEqual('''
parts = []
parts.append('aaa ')
try:
    parts.append(str(a))
except Exception:
    parts.append('{error:a}')
parts.append(' bbb ')
try:
    parts.append(str(b))
except Exception:
    parts.append('{error:b}')
parts.append(' ccc')
result = ''.join(parts)
'''.strip(), source)
    
    def test_with_methods(self):
        source = template._generate_source('aaa {a.lower().capitalize()} bbb')
        self.assertMultiLineEqual('''
parts = []
parts.append('aaa ')
try:
    parts.append(str(a.lower().capitalize()))
except Exception:
    parts.append('{error:a.lower().capitalize()}')
parts.append(' bbb')
result = ''.join(parts)
'''.strip(), source)
    
    def test_expression(self):
        source = template._generate_source('aaa {a + b} bbb')
        self.assertMultiLineEqual('''
parts = []
parts.append('aaa ')
try:
    parts.append(str(a + b))
except Exception:
    parts.append('{error:a + b}')
parts.append(' bbb')
result = ''.join(parts)
'''.strip(), source)
    
    def test_escaping(self):
        source = template._generate_source('"\'\n')
        self.assertMultiLineEqual('''
parts = []
parts.append('"\\'\\n')
result = ''.join(parts)
'''.strip(), source)
        
class TemplateTest(TestCase):
    def test_success(self):
        template = Template('aaa {a + b} bbb')
        result = template(a=1, b=2)
        self.assertEqual('aaa 3 bbb', result)

    def test_failed(self):
        template = Template('aaa {a + c} bbb')
        result = template(a=1, b=2)
        self.assertEqual('aaa {error:a + c} bbb', result)

    def test_bad_syntax(self):
        with self.assertRaises(Exception):
            Template('aaa {!@#$%} bbb')
            