# -*- coding: utf-8 -*-
from decorated.decorators.tempfile import TempFile
from fixtures._fixtures.tempdir import TempDir as TempDirFixture
from fixtures2 import TestCase
import os

class TempFileTest(TestCase):
    def setUp(self):
        super(TempFileTest, self).setUp()
        self.tempdir = self.useFixture(TempDirFixture())
        self.path = self.tempdir.join('111')
        
    def test_never_created(self):
        with TempFile(self.path):
            pass
        self.assertFalse(os.path.exists(self.path))
        
    def test_already_deleted(self):
        _touch(self.path)
        with TempFile(self.path):
            os.remove(self.path)
        self.assertFalse(os.path.exists(self.path))
        
    def test_not_deleted(self):
        _touch(self.path)
        with TempFile(self.path):
            pass
        self.assertFalse(os.path.exists(self.path))
        
    def test_not_delete_on_success(self):
        _touch(self.path)
        with TempFile(self.path, delete_on_success=False):
            pass
        self.assertTrue(os.path.exists(self.path))
        
    def test_not_delete_on_failure(self):
        _touch(self.path)
        try:
            with TempFile(self.path, delete_on_error=False):
                raise Exception()
        except:
            pass
        self.assertTrue(os.path.exists(self.path))
        
    def test_decorator(self):
        @TempFile('{path}')
        def create_file(path):
            _touch(path)
        create_file(self.path)
        self.assertFalse(os.path.exists(self.path))
        
def _touch(path):
    f = open(path, 'w')
    f.close()
    