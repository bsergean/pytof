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

# FIXME: init all loggers in a single place

####
#    Logging (FIXME: factorize that)
####

from log import loggers
# FIXME: find a way to get the file name in python
logger = loggers['ftp']

from ftplib import FTP
from os.path import join, basename
from os import walk, sep, chdir
from sys import exit

class ftpUploader(FTP):
    '''
    For the ftplib manual see http://docs.python.org/lib/ftp-objects.html
    For ftp commands explanations see http://www.nsftools.com/tips/RawFTP.htm
    '''

    def infos(self):
        logger.info('Remote current dir is %s' % self.pwd())

    def ls(self):
        for f in self.nlst('', '-a')[2:]:
            yield f

    def exists(self, fn):
        ''' Test whether file exist in the current remote dir '''
        return basename(fn) in self.ls()

    def upload(self, file):
        fd = open(file)
        # be carefull to leave a space between STOR and the filename
        self.storbinary('STOR ' + basename(file), fd)
        fd.close()

    def lsdir(self, path):

        print path

        lines = []
        def callback(line):
            lines.append(line)

        self.dir('-a %s' % path, callback)

        dirs  = []
        files = []
        for l in lines:
            fn = l.split()[8]
            if l.startswith('d'):

                # FIXME: check with sym link also.
                
                # need to do a better job here since there
                # may be a problem with whitespace dir
                dirs.append( fn )
            else:
                files.append( fn )

        return dirs[2:], files
        
    def rmtree(self, path):
        
        dirs, files = self.lsdir(path)

        for dir in dirs:
            fullpath = join(path, dir)
            self.rmtree(fullpath)
        
        for f in files:
            fullpath = join(path, f)
            print 'remove file', fullpath
            self.delete(fullpath)

        try:
            if path:
                print 'remove dir', os.rmdir(path)
                self.rmd(path)
        except: pass


    def mirror(self, dirname):
        logger.info('mirror (%s)' % dirname)
        remoteDirname = basename(dirname)

        # be carefull, we'll overwrite it:
        # FIXME: add a user input and a force option
        if self.exists(remoteDirname):
            logger.info('Remove dir %s' % remoteDirname)
            self.rmtree(remoteDirname)

        #sys.exit(0)

        logger.info('Create remote dir %s' % remoteDirname)
        self.mkd(remoteDirname)

        logger.info('chdir to remote dir %s' % remoteDirname)
        self.cwd(remoteDirname)

        walkdir = dirname
        for path, subdirs, files in walk(walkdir):
            #print path, subdirs, files

            chdir(path)

            if path != walkdir:
                self.cwd(path.split(walkdir + sep)[1])
            
            for d in subdirs:
                if not self.exists(d):
                    self.mkd(d)

            for f in files:
                self.upload(f)



########
#       Kept for memory but not used anymore
########

#from ftputil import FTPHost
#
#class ftpUploader_fromftputil(FTPHost):
#
#    def infos(self):
#        logger.info('Remote current dir is %s' % self.getcwd())
#
#    def exists(self, fn):
#        ''' Test whether file exist in the current remote dir '''
#        return basename(fn) in self.listdir('.')
#
#    def force_rmtree(self, dirname):
#        ''' rmtree does not seems to work, use our own '''
#        for path, subdirs, files in self.walk(dirname):
#            print path, subdirs, files
#
#    def mirror(self, dirname):
#        logger.info('mirror (%s)' % dirname)
#        remoteDirname = basename(dirname)
#
#        # be carefull, we'll overwrite it:
#        # FIXME: add a user input and a force option
#        if self.exists(remoteDirname):
#            logger.info('Remove dir %s' % remoteDirname)
#            self.rmdir(remoteDirname)
#
#        logger.info('Create remote dir %s' % remoteDirname)
#        self.mkdir(remoteDirname)
#
#        logger.info('chdir to remote dir %s' % remoteDirname)
#        self.chdir(remoteDirname)
#
#        walkdir = dirname
#        # FIXME: hardcoded value
#        walkdir = '/home/bsergean/tmp'
#        for path, subdirs, files in os.walk(walkdir):
#            print path, subdirs, files
#
#            os.chdir(path)
#
#            if path != walkdir:
#                self.chdir(path.split(walkdir + os.sep)[1])
#            
#            for d in subdirs:
#                if not self.exists(d):
#                    self.mkdir(d)
#
#            for f in files:
#                self.upload(f, f)
