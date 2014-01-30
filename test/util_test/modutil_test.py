# -*- coding: utf-8 -*-
from decorated.util import modutil
from unittest.case import TestCase

class LoadModulesTest(TestCase):
    def test(self):
        modutil.load_modules('decorated')
        