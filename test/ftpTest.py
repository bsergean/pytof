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

import sys
sys.path.insert(1, '../pytof')

import unittest

import os
from ftp import ftpUploader
from os.path import join, basename
from os import listdir, lstat, remove, chdir, walk, mkdir
from stat import S_ISDIR
from utils import GetTmpDir, maybemakedirs
from shutil import copy, rmtree
from tempfile import mkdtemp, mktemp

def create(file, content):
    fd = open(file, 'w')
    fd.write(content)
    fd.close()

def diff(a, b):
    ''' Call the real diff function on two Unix files or directories '''
    exitCode = os.system('diff %s %s' % (a, b))
    return exitCode == 0

class FTP_TC(unittest.TestCase):

    def setUp(self):
        self.tempdir = mkdtemp()

        passwd = os.environ.get('PASSWD', '')
        if not passwd:
            print 'no password in $PASSWD'
            sys.exit(1)
        else:
            print 'start ftp connection'
        self.ftp = ftpUploader('localhost', 'bsergean', passwd)

    def tearDown(self):
        rmtree(self.tempdir)

    def testUpLoadOneFile(self):
        tmp = join(self.tempdir, 'b')
        create(tmp, 'youcoulele')

        remoteTmp = mktemp()
        self.ftp.upload(tmp, remoteTmp)
        self.assert_ (diff (tmp, remoteTmp))

    def testMirrorDir(self):
        newDir = 'mirror_dir'
        topDir = join(self.tempdir, newDir)
        maybemakedirs(topDir)
        
        tmpftpfile = 'a_file'
        create(join(self.tempdir, tmpftpfile), 'youcoulele')
        tmpftpfile = 'another_file'
        create(join(self.tempdir, tmpftpfile), 'warzazat')

        nestedDir = join(topDir, 'a_dir')
        mkdir(nestedDir)
        
        tmpftpfile = 'a_file'
        create(join(nestedDir, tmpftpfile), 'youcoulele')
        tmpftpfile = 'another_file'
        create(join(nestedDir, tmpftpfile), 'warzazat')
        
        self.ftp.cp_rf(topDir, self.tempdir)
        self.assert_ (diff (topDir, join(self.tempdir, newDir)))

        
if __name__ == "__main__":
    unittest.main()

    sys.exit(0)
    
    ###########
    # copy -r one dir to another
    print 'mirror'
    ftp.mkd('/home/bsergean/tmp/Capture3D-8.0.0')
    ftp.mirror_r('/usr/local/Adobe/Capture3D-8.0.0', '/home/bsergean/tmp/Capture3D-8.0.0/')
    ftp.rmtree('/home/bsergean/tmp/Capture3D-8.0.0')

    ftp.cp_rf('/usr/local/Adobe/Capture3D-8.0.0', '/home/bsergean/tmp')

    sys.exit(0)

    ###########
    # ftp tests
    # upload a directory

    ###########
    # ftp tests
    # delete a dir
    ftp.rmtree(topDir)
