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

import unittest

import os, sys
from ftp import ftpUploader
from os.path import join, basename, isdir
from os import listdir, lstat, remove, chdir, mkdir
from stat import S_ISDIR
from utils import GetTmpDir, maybemakedirs
from shutil import copy, rmtree
from tempfile import mkdtemp, mktemp
from getpass import getuser

def create(file, content):
    fd = open(file, 'w')
    fd.write(content)
    fd.close()

def diff(a, b):
    ''' Call the real diff function on two Unix files or directories '''
    exitCode = os.system('diff %s %s' % (a, b))
    return exitCode == 0

class FTPTest(unittest.TestCase):
    '''
    This test case needs a local ftp server, and you to set
    the PASSWD env variable to your local account password
    run it like PASSWD=blabla python ftpTest.py
    '''

    def setUp(self):
        self.tempdir = mkdtemp()

        passwd = os.environ.get('PASSWD', '')
        if not passwd:
            print 'no password in $PASSWD'
            sys.exit(1)
        else:
            print 'start ftp connection'
            
        self.ftp = ftpUploader('localhost', getuser(), passwd)
        #self.ftp = ftpUploader('snoball.corp.adobe.com', getuser(), passwd)
        self.ftp.infos()
        self.pwd = self.ftp.pwd()

    def tearDown(self):
        rmtree(self.tempdir)

    def test_upload_one_file(self):
        tmp = join(self.tempdir, 'b')
        create(tmp, 'youcoulele')

        remoteTmp = mktemp()
        self.ftp.upload(tmp, remoteTmp)
        self.assert_ (diff (tmp, remoteTmp))

    def create_dummy_dir(self, newDir):
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

        return topDir

    def test_cp_rf(self):
        newDir = 'mirror_dir'
        topDir = self.create_dummy_dir(newDir)
        self.ftp.cp_rf(topDir, self.tempdir)
        self.assert_(diff(topDir, join(self.tempdir, newDir)))

    def test_rm_tree(self):
        newDir = 'mirror_dir'
        topDir = self.create_dummy_dir(newDir)
        self.ftp.rmtree(topDir)
        self.assert_(not isdir(topDir) )

    def test_mirror_r(self):
        newDir = 'mirror_dir'
        topDir = self.create_dummy_dir(newDir)
        cloneDir = join(self.tempdir, newDir + '2')
        self.ftp.mkd(cloneDir)
        self.ftp.mirror_r(topDir, cloneDir)
        self.assert_(diff(topDir, cloneDir))

