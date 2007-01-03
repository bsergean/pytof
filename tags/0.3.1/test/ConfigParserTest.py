#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- python -*-
#
#*****************************************************************************
#
# See LICENSE file for licensing and to see where does some code come from
#
#*****************************************************************************

__revision__ = '$Id$  (C) 2004 GPL'
__author__ = 'Benjamin Sergeant'

import sys
sys.path.insert(1, '../pytof')

from os import remove
from configFile import configHandler

if __name__ == "__main__":

    conf = configHandler()
    remove(conf.confFilename)
    
    xmlFileName = 'data/AlbumData_gnocchi.xml'

    # this test is bad, we should basically copy some pytof.py code here
    # to do a real caching test (generate the cache the first time, then use it).
