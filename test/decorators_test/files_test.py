# -*- coding: utf-8 -*-
from decorated.decorators.files import TempFile, WritingFile, TempDir
from testutil import TestCase
import os

class TempFileTest(TestCase):
    def setUp(self):
        super(TempFileTest, self).setUp()
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
        
class TempDirTest(TestCase):
    def test(self):
        dirname = self.tempdir.join('111')
        with TempDir(dirname):
            os.mkdir(dirname)
        self.assertFalse(os.path.exists(dirname))
        
class WritingFileTest(TestCase):
    def test_success(self):
        path = self.tempdir.join('111')
        with WritingFile(path) as wf:
            with open(wf.writing_path, 'w') as f:
                f.write('aaa')
        self.assertFalse(os.path.exists(wf.writing_path))
        self.assertEqual('aaa', open(path).read())
        
    def test_error(self):
        path = self.tempdir.join('111')
        with self.assertRaises(Exception):
            with WritingFile(path) as wf:
                with open(wf.writing_path, 'w') as f:
                    f.write('aaa')
                raise Exception()
        self.assertFalse(os.path.exists(wf.writing_path))
        self.assertFalse(os.path.exists(path))
        
    def test_discard(self):
        path = self.tempdir.join('111')
        with WritingFile(path) as wf:
            with open(wf.writing_path, 'w') as f:
                f.write('aaa')
            wf.discard()
        self.assertFalse(os.path.exists(wf.writing_path))
        self.assertFalse(os.path.exists(path))
        
def _touch(path):
    f = open(path, 'w')
    f.close()
    