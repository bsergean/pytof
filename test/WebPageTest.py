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

import os
from os import remove
from utils import GetTmpDir
from makepage import WebPage, PhotoWebPage

if __name__ == "__main__":

    foo = os.path.join(GetTmpDir(), 'foo')
    bar = os.path.join(GetTmpDir(), 'bar')

    wp = WebPage(foo, 'testpage')
    wp.writePage()

    wp = PhotoWebPage(bar, 'bar', 'home.html')
    wp.addSkeleton(12, 12, 1000, ['EXIF infos'], 'back.jpg', 'original',
                   'prev', 'pv_prev', 'next', 'pv_next')
    wp.writePage()

    # here we could try to fetch the photo link from the page
    # and compare the size to check that
    # original_size > medium_size > thumbnail_size
