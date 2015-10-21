# -*- coding: utf-8 -*-
from fixtures._fixtures.tempdir import TempDir
from fixtures2 import TestCase

class TestCase(TestCase):
    def setUp(self):
        super(TestCase, self).setUp()
        self.tempdir = self.useFixture(TempDir())
        