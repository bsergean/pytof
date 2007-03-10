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

import gtkpil as Image

class TestMakeFS(TestCase):

    def setUp(self):
        # FIXME: we shou
        self.tempdir = mkdtemp()
        self.pytofOutput = mktemp(suffix='',
                                  prefix='tmp',
                                  dir=self.tempdir)
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
        image = image.crop((100, 100, 900, 900))
        self.assertEquals(image.size, [800, 800])

    def testResize(self):
        image = Image.open(self.jpgFn)
        image = image.crop((100, 100, 900, 900))

        image2 = Image.open(self.jpgFn)
        image2 = image.resize((800, 800), 'foo')

        self.assertEquals(image.size, image2.size)

    def testRotate(self):
        image = Image.open(self.jpgFn)
        rotatedImage = image.rotate(90)
        [x, y] = self.jpgSize

        self.assertEquals(rotatedImage.size, [y, x])

    def testSave(self):
        image = Image.open(self.jpgFn)
        image.save(self.pytofOutput, 92)

        image2 = Image.open(self.pytofOutput)
