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
from os.path import join
from os import mkdir, listdir, getcwd
from shutil import copy, rmtree
from log import logger

from ezt import Template

class Picture:
    def __init__(self, filename, href):
        self.filename = filename
        self.href = href

class TestMakeFS(TestCase):

    def setUp(self):
        self.tempdir = mkdtemp()
        self.pytof = join('data', 'templates', 'pytof.ezt')
        self.pytofOutput = mktemp()
        print self.pytofOutput

    def tearDown(self):
        rmtree(self.tempdir)
    
    def testOne(self):
        pytofTemplate = Template(self.pytof)

        title = 'template test'
        
        pictures = [Picture('foo.jpg', 'foo.html'),
                    Picture('bar.jpg', 'bar.html')]

        data = { 'title' : title,
                 'pictures' : pictures,
                 }
        data['gallery_name'] = 'Youpi Gallery'

        wfile = open(self.pytofOutput, 'w')
        pytofTemplate.generate(wfile, data)

