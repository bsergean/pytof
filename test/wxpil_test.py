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
from unittest import TestCase
from tempfile import mkdtemp, mktemp
from os.path import join, basename
from os import mkdir, listdir, getcwd
from shutil import copy, rmtree
from log import logger

import wxpil as Image

class TestMakeFS(TestCase):

    def setUp(self):
        self.tempdir = mkdtemp()
        self.pytofOutput = mktemp()

        self.jpgFn = join('data',
                          'fake_iphoto_library',
                          '2005',
                          '03',
                          '23',
                          'rotated_minus_90.jpg')
        self.jpgSize = [1856, 1392]

    def tearDown(self):
        rmtree(self.tempdir)

    def testCreateObject(self):
        image = Image.open(self.jpgFn)
        self.assertEquals(image.size, self.jpgSize)

    def testCrop(self):
        image = Image.open(self.jpgFn)
        image = image.crop(100, 100, 900, 900)
        self.assertEquals(image.size, [800, 800])

        
