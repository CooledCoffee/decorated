# -*- coding: utf-8 -*-
import os
import shutil

from decorated.base.function import ContextFunction
from decorated.base.template import Template


class TempObject(ContextFunction):
    def _after(self, ret, *args, **kw):
        if self._delete_on_success:
            self._do_delete(*args, **kw)
        
    def _calc_path(self, *args, **kw):
        if self._func is None:
            return self._path()
        else:
            arg_dict = self._resolve_args(*args, **kw)
            return self._path(**arg_dict)

    def _delete(self, path):
        raise NotImplementedError()
    
    def _do_delete(self, *args, **kw):
        path = self._calc_path(*args, **kw)
        if not os.path.exists(path):
            return
        self._delete(path)
    
    def _error(self, error, *args, **kw):
        if self._delete_on_error:
            self._do_delete(*args, **kw)
        
    def _init(self, path, delete_on_success=True, delete_on_error=True): # pylint: disable=arguments-differ
        super(TempObject, self)._init()
        self._path = Template(path)
        self._delete_on_success = delete_on_success
        self._delete_on_error = delete_on_error
        
class TempFile(TempObject):
    def _delete(self, path):
        os.remove(path)
            
class TempDir(TempObject):
    def _delete(self, path):
        shutil.rmtree(path)

class WritingFile(ContextFunction):
    def discard(self):
        self._discarded = True
        
    def _init(self, path): # pylint: disable=arguments-differ
        super(WritingFile, self)._init()
        self.path = path
        self.writing_path = self.path + '.writing'
        self._discarded = False
        
    def _after(self, ret, *args, **kw):
        if self._discarded:
            os.remove(self.writing_path)
        else:
            shutil.move(self.writing_path, self.path)
    
    def _error(self, error, *args, **kw):
        os.remove(self.writing_path)
    