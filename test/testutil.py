# -*- coding: utf-8 -*-
from fixtures._fixtures.tempdir import TempDir
from fixtures2 import TestCase


class DecoratedTest(TestCase):
    # noinspection PyAttributeOutsideInit
    def setUp(self):
        super(DecoratedTest, self).setUp()
        self.tempdir = self.useFixture(TempDir())
