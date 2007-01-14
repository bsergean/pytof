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
from utils import RemoveSpecificChars, UnixFind, urlExtractor, mktar, maybemakedirs
from os.path import join, getsize
from tempfile import mkdtemp, mktemp
from shutil import rmtree, copytree
from os import mkdir
import tarfile

class TestUtils(TestCase):

    def setUp(self):
        self.tempdir = mkdtemp()
        self.baseDir = join('data', 'galleries')

#    def tearDown(self):
#        rmtree(self.tempdir)
    
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

    def create_dummy_dir(self, newDir):
        '''
        This one is duplicated from ftp_utils: We should create a class
        that inherit unittest.TestCase, with this method in it in test.py.
        We should take care of the self.tmpdir also.
        '''

        def create(file, content):
            fd = open(file, 'w')
            fd.write(content)
            fd.close()
        
        topDir = join(self.tempdir, newDir)
        maybemakedirs(topDir)

        # first level
        tmpftpfile = 'a_file'
        create(join(self.tempdir, tmpftpfile), 'youcoulele')
        tmpftpfile = 'another_file'
        create(join(self.tempdir, tmpftpfile), 'warzazat')

        # second level
        tmpftpfile = 'one_file'
        create(join(topDir, tmpftpfile), 'youcoulele')

        # third level
        nestedDir = join(topDir, 'a_dir')
        mkdir(nestedDir)

        tmpftpfile = 'a_file'
        create(join(nestedDir, tmpftpfile), 'youcoulele')
        tmpftpfile = 'another_file'
        create(join(nestedDir, tmpftpfile), 'warzazat')

        return topDir
    
    def testTar(self):
        '''
        Create an archve from a temp dir created with create_dummy_dir
        put one file at the prefix level, tar the archive
        extract the archive, and check that the file is there and
        that its size is the same as the original one.
        '''
        
        dummyDir = self.create_dummy_dir('tar_test_dir')
        tmpftpfile = 'one_file'
        topLevelFile = join(dummyDir, tmpftpfile)
        topLevelFileSize = getsize(topLevelFile)
        
        tarFile = join(self.tempdir, 'foo.bar')
        mktar(tarFile, dummyDir, 'a_dir', [topLevelFile])

        # now list the file within the archive and look for topLevelFile
        tar = tarfile.open(tarFile)
        found = False
        for tarinfo in tar:
            if tarinfo.name == tmpftpfile:
                found = True
                size = tarinfo.size
                break

        self.assert_(found)
        self.assertEquals(size, topLevelFileSize)
