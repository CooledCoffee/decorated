# -*- coding: utf-8 -*-

class Proxy(object):
    def __init__(self, target=None):
        super(Proxy, self).__init__()
        self._orig_target = target
        
    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        else:
            target = self._target()
            if target:
                try:
                    return getattr(target, name)
                except AttributeError:
                    raise AttributeError("'%s' object has no attribute '%s'" % (type(self).__name__, name))
            else:
                raise AttributeError('%s object has no attribute "%s", and target is not available.' % (type(self), name))
    
    def _target(self):
        return self._orig_target
    