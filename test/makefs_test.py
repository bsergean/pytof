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
from unittest import TestCase
from tempfile import mkdtemp, mktemp
from os.path import join
from os import mkdir, listdir, getcwd
from shutil import copy, rmtree
from log import logger

from albumdataparser import AlbumDataParser
from makefs import main

class TestMakeFS(TestCase):

    def setUp(self):
        self.tempdir = mkdtemp()
        self.albumName = 'Youpi gallery'
        self.topDir = self.tempdir
        self.libraryPath = join('data', 'fake_iphoto_library')
        self.xmlFilename = 'AlbumData_fake_iphoto-2.xml'

    def tearDown(self):
        rmtree(self.tempdir)
    
    def testOnlyPNG(self):

        parser = AlbumDataParser(self.libraryPath, self.xmlFilename)
        self.xmlData = parser.parse()

        albumList = self.xmlData.getAlbumList()
        self.assertEquals(albumList[0], 'Youpi gallery')
        
        main(self.albumName, self.topDir, self.xmlData)

        # FIXME: test that the output directory contains our picture
