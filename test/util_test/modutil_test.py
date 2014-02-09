# -*- coding: utf-8 -*-
from decorated.util import modutil
from unittest.case import TestCase

class LoadTreeTest(TestCase):
    def test_package(self):
        modutil.load_tree('decorated')
        
    def test_module(self):
        modutil.load_tree('decorated.util.modutil')
        