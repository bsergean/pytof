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

import os
from ftp import ftpUploader
from os.path import join, basename
from utils import GetTmpDir, maybemakedirs

import stat
# stolen and adapted from shutils rmtree
def my_rmtree(path):
    try:
        names = os.listdir(path)
    except:
        pass
    for name in names:
        fullname = os.path.join(path, name)
        try:
            mode = os.lstat(fullname).st_mode
        except: pass
        if stat.S_ISDIR(mode):
            rmtree(fullname)
        else:
            try:
                os.remove(fullname)
            except: pass
    try:
        os.rmdir(path)
    except: pass

def create(file, content):
    fd = open(file, 'w')
    fd.write(content)
    fd.close()

if __name__ == "__main__":
    
    ###########
    # ftp tests
    # upload a file
    tmpDir = GetTmpDir()
    
    tmpftpfile = 'b'
    create(tmpftpfile, 'youcoulele')

    # this test needs the ftp password to be stored
    # in the PASSWD env variable
    passwd = os.environ.get('PASSWD', '')
    if not passwd:
        print 'no password in $PASSWD'
        sys.exit(1)
    else:
        print 'start ftp connection'
    
    ftp = ftpUploader('localhost', 'bsergean', passwd)
    ftp.infos()
    for f in ftp.ls():
        print f

    ###########
    # ftp tests
    # upload a directory
    topDir = join(tmpDir, 'mirror_dir')
    maybemakedirs(topDir)
    
    tmpftpfile = 'a_file'
    create(join(topDir, tmpftpfile), 'youcoulele')
    tmpftpfile = 'another_file'
    create(join(topDir, tmpftpfile), 'warzazat')

    nestedDir = join(topDir, 'a_dir')
    maybemakedirs(nestedDir)

    tmpftpfile = 'a_file'
    create(join(nestedDir, tmpftpfile), 'youcoulele')
    tmpftpfile = 'another_file'
    create(join(nestedDir, tmpftpfile), 'warzazat')

    ftp.mirror(topDir)
