# -*- coding: utf-8 -*-
from decorated.base.function import Function
import logging

log = logging.getLogger(__name__)

class IgnoreError(Function):
    def _call(self, *args, **kw):
        try:
            return super(IgnoreError, self)._call(*args, **kw)
        except:
            log.warn('Exception ignored.', exc_info=True)
    