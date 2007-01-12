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

from unittest import TestCase
from makepage import main
from tempfile import mkdtemp, mktemp
from os.path import join
from os import mkdir, listdir
from shutil import copy

class TestMakeGalleryFromDir(TestCase):

    def setUp(self):
        self.tempdir = mkdtemp()
        self.albumName = 'Youpi'
        self.topDir = self.tempdir
        self.xmlData = None
        self.strip_originals = False
        self.baseDir = join('data', 'galleries')

        self.jpgsDir = join(self.baseDir, 'xxdiff-3.2-screenshots')
        self.pngDir = join(self.baseDir, 'recoll-icons')
    
    def testOnlyPNG(self):

        main(self.albumName, self.topDir, self.xmlData, self.strip_originals,
             fromDir = self.pngDir)

    def testOnlyJPG(self):

        main(self.albumName, self.topDir, self.xmlData, self.strip_originals,
             fromDir = self.jpgsDir)

    def testOnlyMixedSimple(self):
        ''' I am happy I wrote this one because I found a bug :) '''

        src = join(self.tempdir, 'mixedSimple')

        print src
        mkdir(src)

        for d in [self.jpgsDir, self.pngDir]:
            for f in listdir(d)[0:2]:
                copy(join(d, f), src)

        main(self.albumName, self.topDir, self.xmlData, self.strip_originals,
             fromDir = src)

    def testOnlyMixedFull(self):
        ''' I am happy I wrote this one because I found a bug :) '''

        src = join(self.tempdir, 'mixedFull')

        print src
        mkdir(src)

        for d in [self.jpgsDir, self.pngDir]:
            for f in listdir(d):
                copy(join(d, f), src)

        main(self.albumName, self.topDir, self.xmlData, self.strip_originals,
             fromDir = src)
        

# For the computer history museum:
#
#        # dont want to think, it's late ...
#        class gotoException(Exception): pass
#        for d in [self.jpgsDir, self.pngDir]:
#            try:
#                for f in listdir(d):
#                    copy(join(d, f), src)
#                    raise gotoException
#            except (gotoException): pass
