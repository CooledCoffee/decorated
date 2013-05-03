# -*- coding: utf-8 -*-

class Proxy(object):
    def __init__(self, target=None):
        super(Proxy, self).__init__()
        self.__target = target
        
    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        else:
            target = self._target()
            return getattr(target, name)
    
    def _target(self):
        if not self.__target:
            raise Exception('%s has no target.' % type(self).__name__)
        return self.__target
    