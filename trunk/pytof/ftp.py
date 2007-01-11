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

from log import loggers
# FIXME: find a way to get the file name in python
logger = loggers['ftp']

from os.path import join, basename
from os import walk, sep, chdir, rmdir, getcwd, listdir, lstat, mkdir, makedirs
from sys import exc_info
from stat import S_ISDIR, S_ISLNK
from utils import notYetImplemented
from ftplib import FTP, error_temp, all_errors

class ftpUploader(FTP):
    '''
    For the ftplib manual see http://docs.python.org/lib/ftp-objects.html
    For ftp commands explanations see http://www.nsftools.com/tips/RawFTP.htm
    '''

    def __init__(self, host, user, password):
        ''' Start the connection '''
        self.ok = False
        try:
            FTP.__init__(self, host, user, password)
            self.ok
        except all_errors, msg:
            logger.error(msg)

    def infos(self):
        if not self.ok: return
        logger.info('Remote current ftp identification: %s' % self.getwelcome())

    def exists(self, fn):
        ''' Test whether file exist '''
        if not self.ok: return
        logger.debug('Does %s exists' % fn)
        try:
            def callback(line): pass
            self.dir('-a %s' % fn, callback)
            return True
        except error_temp:
            return False

    def upload(self, src, tget = None):
        ''' Caution: no error handling '''
        if not self.ok: return
        fd = open(src)
        # be carefull to leave a space between STOR and the filename
        if not tget:
            target = basename(src)
        self.storbinary('STOR ' + target, fd)
        fd.close()

    def lsdir(self, path):
        '''
        List files within the "path" directory
        We use the non-standard -a to get filename
        starting with a dot (like .bashrc)
        '''
        if not self.ok: return
        logger.debug('lsdir %s' % path)

        lines = []
        def callback(line):
            lines.append(line)

        self.dir('-a %s' % path, callback)

        files = []
        for l in lines:
            # need to do a better job here since there
            # may be a problem with file containing whitespace
            logger.debug('Current line: %s' % l)
            fn = l.split()[8]
            if l.startswith('d'):
                files.append( (fn, 'Directory') )
            elif l.startswith('l'):
                files.append( (fn, 'Symbolic link') )                
            else:
                files.append( (fn, 'Regular File') )

        return files[2:]

    def rmtree(self, path):
        if not self.ok: return
        if not self.exists(path): return
        self.rmtree_r(path)
        
    def rmtree_r(self, path):
        '''
        Caution: This method depends on lsdir which may be buggy (symlinks)
        Recursive, inspired from shutil.rmtree
        '''
        if not self.ok: return
        files = self.lsdir(path)
        logger.debug(files)

        for f, fileType in files:
            fullpath = join(path, f)

            if fileType == 'Directory':
                logger.info('recurse on %s' % fullpath)
                self.rmtree_r(fullpath)
            elif fileType == 'Regular File':
                logger.info('remove file %s' % fullpath)
                self.delete(fullpath)

        if path:
            logger.info('remove dir %s' % path)
            self.rmd(path)

    def cp_rf(self, src, tget):
        if not self.ok: return
        src_basename = basename(src)
        full_tget = join(tget, src_basename)
        self.rmtree(full_tget)
        self.mkd(full_tget)
        self.mirror_r(src, full_tget)

    def mirror_r(self, src, tget):
        ''' Recursive version '''
        if not self.ok: return
        names = listdir(src)
        logger.debug(names)

        for name in names:
            fullname = join(src, name)
            r_fullname = join(tget, name)
            try:
                mode = lstat(fullname).st_mode
            except: pass
            if S_ISDIR(mode):
                mkdir(r_fullname)
                self.mirror_r(fullname, r_fullname)
            elif S_ISLNK(mode):
                # FIXME
                #notYetImplemented()
                pass
            else:
                self.upload(fullname, r_fullname)
