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

from ezt import Template

class TestMakeFS(TestCase):

    def setUp(self):
        self.tempdir = mkdtemp()
        self.pytof = join('data', 'templates', 'pytof.ezt')
        self.perpage = join('data', 'templates', 'photo_per_page.ezt')
        self.index = join('data', 'templates', 'gallery_index.ezt')
        self.pytofOutput = mktemp()
        #print self.pytofOutput

    def tearDown(self):
        rmtree(self.tempdir)
