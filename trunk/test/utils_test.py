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

# FIXME: see the run function at the bottom.
import sys
sys.path.insert(1, '../pytof')
    
from unittest import TestCase
from utils import RemoveSpecificChars, UnixFind, urlExtractor
from utils import mkarchive, maybemakedirs, lpathstrip, chmodwwdir, create
from os.path import join, getsize
import tarfile
from zipfile import ZipFile, ZIP_DEFLATED
from log import quiet
from test import PytofTestCase
from tempfile import mkdtemp
from shutil import rmtree
import os

#quiet()

class TestUtils(PytofTestCase):
    
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
        self.assertEquals(len(UnixFind(join(self.galleries, 'recoll-icons'), '.png')), 12)
        self.assertEquals(len(UnixFind(join(self.galleries, 'xxdiff-3.2-screenshots'), '.jpg')), 22)

    def testUrlExtractor(self):
        '''
        In the long run this would be a test to check that urls within
        the HTML we generate is not broken.
        '''
        leschats = join(self.galleries, 'Les_chats_html_only')

        for url in urlExtractor(join(leschats, 'index.html')):
            self.assertEquals(url, 'http://code.google.com/p/pytof/')
    
    def testTar(self):
        '''
        Create an archve from a temp dir created with create_dummy_dir
        put one file at the prefix level, tar the archive
        extract the archive, and check that the file is there and
        that its size is the same as the original one.

        FIXME: we should check for other files at other levels in the tar hierarchy.
        '''
        
        dummyDir = self.create_dummy_dir('tar_test_dir')
        tmpftpfile = 'level_2_fileA'
        topLevelFile = join(dummyDir, tmpftpfile)
        topLevelFileSize = getsize(topLevelFile)
        
        tarFile = join(self.tempdir, 'foo.tar')
        mkarchive(tarFile, dummyDir, 'a_dir', [topLevelFile], Zip = False, tar = True)

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

        
    def testZip(self):
        dummyDir = self.create_dummy_dir('tar_test_dir')
        tmpftpfile = 'level_2_fileA'
        topLevelFile = join(dummyDir, tmpftpfile)
        topLevelFileSize = getsize(topLevelFile)
        
        zipFile = join(self.tempdir, 'foo.zip')
        mkarchive(zipFile, dummyDir, 'a_dir', [topLevelFile])
        # you also have printdirs to have a ls like output
        # of the content of the zip file
        self.assert_(tmpftpfile in ZipFile(zipFile).namelist())

        # TODO: use sets.Set to do differences between the two sets of files (in the
        # archive and in the dir)


    def testlpathstrip(self):
        '''
        Make sure the coverage is ok
        '''
        prefix = self.tempdir + os.sep
        path = join(self.tempdir, 'kiki', 'coucou')
        self.assertEquals(lpathstrip(prefix, path), join('kiki', 'coucou'))

        prefix = self.tempdir
        self.assertEquals(lpathstrip(prefix, path), join('kiki', 'coucou'))

    def testchmod(self):
        foodir = mkdtemp()
        chmodwwdir(foodir)
        rmtree(foodir)

def run():
    '''
    Should be in test and detect the current test name automatically.
    Need this for IDLE on Windows where you can execute a with F5 and
    where the shell/terminal support is bad and it's 
    a hassle to start test from command line.
    '''
    import unittest
    testModules = ['utils_test']
    alltests = unittest.TestLoader().loadTestsFromNames(testModules)
    unittest.TextTestRunner().run(alltests)
    
if __name__ == '__main__':
    run()
