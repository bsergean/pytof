#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- python -*-
#
#*****************************************************************************
#
# See LICENSE file for licensing and to see where does some code come from
#
#*****************************************************************************

__revision__ = '$Id$  (C) 2007 GPL'


from unittest import TestCase
from utils import RemoveSpecificChars, UnixFind, urlExtractor
from os.path import join
from tempfile import mkdtemp, mktemp

class TestUtils(TestCase):

    def setUp(self):
        self.tempdir = mkdtemp()
        self.baseDir = join('data', 'galleries')
    
    def testRemoveSpecificChars(self):
        testCases = [
            ["test1", "test1"],
            ["test2(", "test2"]]
        for case in testCases:
            self.assertEquals(case[1], RemoveSpecificChars(case[0]))

    def testUnixFind(self):
        '''
        [bsergean@marge1 test]$ find data/galleries/recoll-icons/ -name '*.png' | wc -l
        12
        [bsergean@marge1 test]$ find data/galleries/xxdiff-3.2-screenshots/ -name '*.jpg' | wc -l
        22
        '''
        galleries = join('data', 'galleries')
        self.assertEquals(len(UnixFind(join(galleries, 'recoll-icons'), '.png')), 12)
        self.assertEquals(len(UnixFind(join(galleries, 'xxdiff-3.2-screenshots'), '.jpg')), 22)

    def testUrlExtractor(self):
        '''
        In the long run this would be a test to check that urls within
        the HTML we generate is not broken.
        '''
        leschats = join(self.baseDir, 'Les_chats_html_only')

        for url in urlExtractor(join(leschats, 'index.html')):
            self.assertEquals(url, 'http://code.google.com/p/pytof/')
