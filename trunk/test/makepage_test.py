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

import os
from utils import GetTmpDir
from makepage import WebPage, PhotoWebPage, main
from unittest import TestCase
from tempfile import mkdtemp, mktemp
from os.path import join
from os import mkdir, listdir, getcwd
from shutil import copy, rmtree
from log import MainLogger

# comment me if you want to enable logging
MainLogger.quiet()


class PhotoWebPageTest(TestCase):
    def testWritePage(self):
        foo = os.path.join(GetTmpDir(), 'foo')
        bar = os.path.join(GetTmpDir(), 'bar')

        wp = WebPage(foo, 'testpage')
        wp.writePage()

        wp = PhotoWebPage(bar, 'bar', 'home.html')

        # addSkeleton use a dictionnary now
        #wp.addSkeleton(12, 12, 1000, ['EXIF infos'], 'back.jpg', 'original',
        #               'prev', 'pv_prev', 'next', 'pv_next')
        wp.writePage()

        # here we could try to fetch the photo link from the page
        # and compare the size to check that
        # original_size > medium_size > thumbnail_size

        self.assert_(True)


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

    def tearDown(self):
        rmtree(self.tempdir)
    
    def testOnlyPNG(self):

        main(self.albumName, self.topDir, self.xmlData, self.strip_originals,
             fromDir = self.pngDir)

    def testOnlyJPG(self):

        main(self.albumName, self.topDir, self.xmlData, self.strip_originals,
             fromDir = self.jpgsDir)

    def testOnlyMixedSimple(self):
        '''
        I am happy I wrote this one because I found a bug :)
        Only take two picture of the jpeg and png sets
        '''

        src = join(self.tempdir, 'mixedSimple')
        mkdir(src)

        for d in [self.jpgsDir, self.pngDir]:
            # the first file is the .svn dir ... start at 1, big hack
            for f in listdir(d)[1:3]:
                copy(join(d, f), src)

        main(self.albumName, self.topDir, self.xmlData, self.strip_originals,
             fromDir = src)

    def testOnlyMixedFull(self):
        ''' Mix all png and jpeg in a single dir '''

        src = join(self.tempdir, 'mixedFull')
        mkdir(src)

        for d in [self.jpgsDir, self.pngDir]:
            # the first file is the .svn dir ... start at 1, big hack            
            for f in listdir(d)[1:]:
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
