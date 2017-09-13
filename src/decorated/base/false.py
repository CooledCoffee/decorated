# -*- coding: utf-8 -*-

class FalseObject(object):
    '''
    >>> bool(FalseObject())
    False
    '''

    def __bool__(self):
        return False

    def __nonzero__(self):
        return False

NOTSET = FalseObject()
