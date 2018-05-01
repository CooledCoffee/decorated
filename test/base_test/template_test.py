# -*- coding: utf-8 -*-
import six

from decorated.base import template
from decorated.base.template import Template
from testutil import DecoratedTest

class GenerateSourceTest(DecoratedTest):
    def test_single_string(self):
        source = template._generate_source('aaa')
        self.assertMultiLineEqual('''
parts = []
parts.append(u'aaa')
result = ''.join(parts)
'''.strip(), source)
    
    def test_single_variable(self):
        source = template._generate_source('{a}')
        expected = '''
parts = []
try:
    parts.append(%s(a))
except Exception:
    parts.append(u'{error:a}')
result = ''.join(parts)
''' % template._DEFAULT_STRING_TYPE
        self.assertMultiLineEqual(expected.strip(), source)
    
    def test_multi_variables(self):
        source = template._generate_source('{a}{b}')
        expected = '''
parts = []
try:
    parts.append(%s(a))
except Exception:
    parts.append(u'{error:a}')
try:
    parts.append(%s(b))
except Exception:
    parts.append(u'{error:b}')
result = ''.join(parts)
''' % (template._DEFAULT_STRING_TYPE, template._DEFAULT_STRING_TYPE)
        self.assertMultiLineEqual(expected.strip(), source)
    
    def test_strings_and_variables(self):
        source = template._generate_source('aaa {a} bbb {b} ccc')
        expected = '''
parts = []
parts.append(u'aaa ')
try:
    parts.append(%s(a))
except Exception:
    parts.append(u'{error:a}')
parts.append(u' bbb ')
try:
    parts.append(%s(b))
except Exception:
    parts.append(u'{error:b}')
parts.append(u' ccc')
result = ''.join(parts)
''' % (template._DEFAULT_STRING_TYPE, template._DEFAULT_STRING_TYPE)
        self.assertMultiLineEqual(expected.strip(), source)
        
    def test_unicode(self):
        source = template._generate_source(u'一{u"二"}三')
        expected = u'''
parts = []
parts.append(u'一')
try:
    parts.append(%s(u"二"))
except Exception:
    parts.append(u'{error:u"二"}')
parts.append(u'三')
result = ''.join(parts)
''' % template._DEFAULT_STRING_TYPE
        self.assertMultiLineEqual(expected.strip(), source)
    
    def test_with_methods(self):
        source = template._generate_source('aaa {a.lower().capitalize()} bbb')
        expected = '''
parts = []
parts.append(u'aaa ')
try:
    parts.append(%s(a.lower().capitalize()))
except Exception:
    parts.append(u'{error:a.lower().capitalize()}')
parts.append(u' bbb')
result = ''.join(parts)
''' % template._DEFAULT_STRING_TYPE
        self.assertMultiLineEqual(expected.strip(), source)
    
    def test_expression(self):
        source = template._generate_source('aaa {a + b} bbb')
        expected = '''
parts = []
parts.append(u'aaa ')
try:
    parts.append(%s(a + b))
except Exception:
    parts.append(u'{error:a + b}')
parts.append(u' bbb')
result = ''.join(parts)
''' % template._DEFAULT_STRING_TYPE
        self.assertMultiLineEqual(expected.strip(), source)
    
    def test_escaping(self):
        source = template._generate_source('"\'\n')
        self.assertMultiLineEqual('''
parts = []
parts.append(u'"\\'\\n')
result = ''.join(parts)
'''.strip(), source)
        
class TemplateTest(DecoratedTest):
    def test_success(self):
        template = Template('aaa {a + b} bbb')
        result = template(a=1, b=2)
        self.assertEqual('aaa 3 bbb', result)

    def test_unicode(self):
        template = Template(u'一{u"二"}三')
        result = template(a=1, b=2)
        self.assertEqual(u'一二三', result)
        
    def test_failed(self):
        template = Template('aaa {a + c} bbb')
        result = template(a=1, b=2)
        self.assertEqual('aaa {error:a + c} bbb', result)

    def test_bad_syntax(self):
        with self.assertRaises(Exception):
            Template('aaa {!@#$%} bbb')
        