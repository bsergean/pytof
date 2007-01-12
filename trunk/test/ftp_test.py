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
from ftplib import all_errors
from os.path import join, basename, isdir
from os import listdir, lstat, remove, chdir, mkdir
from stat import S_ISDIR
from utils import GetTmpDir, maybemakedirs
from shutil import copy, rmtree
from tempfile import mkdtemp, mktemp
from getpass import getuser
from log import logger, quiet

# comment me if you want to debug here
quiet()

def create(file, content):
    fd = open(file, 'w')
    fd.write(content)
    fd.close()

def diff(a, b):
    ''' Call the real diff function on two Unix files or directories '''
    exitCode = os.system('diff %s %s > /dev/null' % (a, b))
    return exitCode == 0

# FIXME: both class should inherit from the same class for factorization

class FTPTestLocal(unittest.TestCase):
    '''
    This test case needs a local ftp server, and you to set
    the PASSWD env variable to your local account password
    run it like PASSWD=blabla python test.py -t ftp_test.FTPTestLocal
    '''

    def setUp(self):
        self.tempdir = mkdtemp()
        self.ok = False

        passwd = os.environ.get('PASSWD', '')
        if not passwd:
            logger.warn('no password in $PASSWD')
            
        self.ftp = ftpUploader('localhost', getuser(), passwd)
        if not self.ftp.ok:
            return
        self.ok = True

        #self.ftp = ftpUploader('snoball.corp.adobe.com', getuser(), passwd)
        self.ftp.infos()
        self.pwd = self.ftp.pwd()

    def tearDown(self):
        if not self.ok: return
        rmtree(self.tempdir)

    def test_upload_one_file(self):
        if not self.ok: return
        tmp = join(self.tempdir, 'b')
        create(tmp, 'youcoulele')

        remoteTmp = mktemp()
        self.ftp.upload(tmp, remoteTmp)
        self.assert_ (diff (tmp, remoteTmp))

    def create_dummy_dir(self, newDir):
        if not self.ok: return
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
        if not self.ok: return
        newDir = 'mirror_dir'
        topDir = self.create_dummy_dir(newDir)
        self.ftp.cp_rf(topDir, self.tempdir)
        self.assert_(diff(topDir, join(self.tempdir, newDir)))

    def test_rm_tree(self):
        if not self.ok: return
        newDir = 'mirror_dir'
        topDir = self.create_dummy_dir(newDir)
        self.ftp.rmtree(topDir)
        self.assert_(not isdir(topDir) )

    def test_mirror_r(self):
        if not self.ok: return
        newDir = 'mirror_dir'
        topDir = self.create_dummy_dir(newDir)
        cloneDir = join(self.tempdir, newDir + '2')
        self.ftp.mkd(cloneDir)
        self.ftp.mirror_r(topDir, cloneDir)
        self.assert_(diff(topDir, cloneDir))


class FTPTestRemote(unittest.TestCase):
    '''
    This test case needs a remote ftp server, and you to set
    the PASSWD env variable to your local account password
    run it like PASSWD=blabla python test.py -t ftp_test.FTPTestRemote
    '''

    def setUp(self):
        self.tempdir = mkdtemp()
        self.ok = False

        passwd = os.environ.get('PASSWD', '')
        if not passwd:
            logger.warn('no password in $PASSWD')
            
        self.ftp = ftpUploader('lisa1', getuser(), passwd)
        if not self.ftp.ok:
            return
        self.ok = True

        #self.ftp = ftpUploader('snoball.corp.adobe.com', getuser(), passwd)
        self.ftp.infos()
        self.pwd = self.ftp.pwd()

        # create remote dummy dir
        self.remoteDir = basename(self.tempdir)
        self.ftp.mkd(self.remoteDir)

    def tearDown(self):
        '''
        Delete the local tree
        FIXME: We should also delete the remote tree
        '''
        if not self.ok: return
        rmtree(self.tempdir)
        self.ftp.rmtree(self.remoteDir)

    def create_dummy_dir(self, newDir):
        if not self.ok: return
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

    def info():
        if not self.ok: return
        self.ftp.infos()

    def test_upload_one_file(self):
        if not self.ok: return
        tmp = join(self.tempdir, 'b')
        create(tmp, 'youcoulele')

        remoteTmp = basename(mktemp())
        self.ftp.upload(tmp, join(self.remoteDir, remoteTmp))

    def test_cp_rf(self):
        if not self.ok: return
        newDir = 'mirror_dir'
        topDir = self.create_dummy_dir(newDir)
        self.ftp.cp_rf(topDir, self.remoteDir)

