#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- python -*-
#
#*****************************************************************************
#
# See LICENSE file for licensing and to see where does some code come from
#
#*****************************************************************************

__revision__ = '$Id: utils.py 67 2006-12-22 22:53:55Z bsergean $  (C) 2004 GPL'
__author__ = 'Benjamin Sergeant'

import sys
sys.path.insert(1, '../pytof')

from os import remove
from makepage import WebPage

if __name__ == "__main__":

    wp = WebPage('out', 'testpage')
    wp.writePage()
