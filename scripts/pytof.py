#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- python -*-
#*****************************************************************************
#
# See LICENSE file for licensing and to see where does some code come from
#
#*****************************************************************************
#
# Main file.
#

__revision__ = '$Id$  (C) 2006 GPL'
__author__ = 'Benjamin Sergeant'
__dependencies__ = []

import sys
sys.path.insert(1, '../pytof')

from options import pytofOptions
from pytofmain import Pytof

if __name__ == "__main__":
    # Import Psyco if available
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass

    po = pytofOptions()
    po.check()
    pytof = Pytof(po)
    pytof.main()

