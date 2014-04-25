# -*- coding: utf-8 -*-

class Proxy(object):
    def __init__(self, target=None):
        super(Proxy, self).__init__()
        self._target = target
        
    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        else:
            try:
                return getattr(self.target, name)
            except NoTargetError:
                raise AttributeError("'%s' object has no attribute '%s'" % (type(self).__name__, name))
            except AttributeError:
                raise AttributeError("'%s' object has no attribute '%s'" % (type(self).__name__, name))
            
    @property
    def target(self):
        if self._target is None:
            raise NoTargetError()
        return self._target

class NoTargetError(Exception):
    pass
