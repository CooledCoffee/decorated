# -*- coding: utf-8 -*-
import threading

class ThreadLocal(object):
    def __init__(self, default=None):
        super(ThreadLocal, self).__init__()
        self._data = threading.local()
        self._default = default
    
    def get(self):
        try:
            return self._data.value
        except AttributeError:
            return self._default
    
    def set(self, value):
        self._data.value = value
        
    def reset(self):
        del self._data.value
    