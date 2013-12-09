# -*- coding: utf-8 -*-
import sys

IS_PYTHON3 = sys.version_info.major == 3

if IS_PYTHON3:
    import builtins  # @UnresolvedImport @UnusedImport
    STRING_TYPE = builtins.str
else:
    import __builtin__
    STRING_TYPE = __builtin__.basestring
    