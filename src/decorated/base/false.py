# -*- coding: utf-8 -*-

class FalseObject(object):
    def __nonzero__(self):
        '''
        >>> bool(FalseObject())
        False
        '''
        return False

NOTSET = FalseObject()
