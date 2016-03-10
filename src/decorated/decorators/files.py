# -*- coding: utf-8 -*-
from decorated.base.function import ContextFunction
import os
import shutil

class TempObject(ContextFunction):
    def _after(self, ret, *args, **kw):
        if self._delete_on_success:
            self._do_delete(*args, **kw)
        
    def _calc_path(self, *args, **kw):
        if self._func is None:
            return self._path
        else:
            d = self._resolve_args(*args, **kw)
            return self._path.eval(d)
                
    def _decorate(self, func):
        super(TempObject, self)._decorate(func)
        self._path = self._compile_template(self._path)
        return self
    
    def _do_delete(self, *args, **kw):
        path = self._calc_path(*args, **kw)
        if not os.path.exists(path):
            return
        self.delete(path)
    
    def _error(self, err, *args, **kw):
        if self._delete_on_error:
            self._do_delete(*args, **kw)
        
    def _init(self, path, delete_on_success=True, delete_on_error=True):
        super(TempObject, self)._init()
        self._path = path
        self._delete_on_success = delete_on_success
        self._delete_on_error = delete_on_error
        
class TempFile(TempObject):
    delete = os.remove
            
class TempDir(TempObject):
    delete = shutil.rmtree

class WritingFile(ContextFunction):
    def discard(self):
        self._discarded = True
        
    def _init(self, path):
        super(WritingFile, self)._init()
        self.path = path
        self.writing_path = self.path + '.writing'
        self._discarded = False
        
    def _after(self, ret, *args, **kw):
        if self._discarded:
            os.remove(self.writing_path)
        else:
            shutil.move(self.writing_path, self.path)
    
    def _error(self, err, *args, **kw):
        os.remove(self.writing_path)
    