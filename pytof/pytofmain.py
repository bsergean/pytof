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

from log import logger, quiet
from os.path import expanduser, join, exists, basename, isabs, walk, isdir
from albumdataparser import AlbumDataParser, AlbumDataParserError
import os, sys
from utils import _err_, _err_exit, echo, GetTmpDir, mkarchive
from config import configHandler
import makepage, makefs
from shutil import rmtree
from ftp import ftpUploader, ftpPush
from ftplib import error_perm
from getpass import getuser, unix_getpass
from string import rstrip

class Pytof(object): pass

def main(albumName, libraryPath, xmlFileName, outputDir,
         info, fs, tar, Zip, ftp, strip_originals, fromDir):
    # init the config file
    conf = configHandler()
    if not conf.ok:
        _err_exit('Problem with the config file')

    libraryPath, xmlFileName, outputDir = \
                 conf.getValuesAndUpdateFromUser(libraryPath, xmlFileName, outputDir)

    ##
    # get iPhoto datas or flat dir pictures list
    if not fromDir:
        try:
            adp = AlbumDataParser(libraryPath, xmlFileName)
            xmlData = adp.maybeLoadFromXML(conf)
            
        except(AlbumDataParserError):
            _err_exit("Problem parsing AlbumData.xml")
    else:
        logger.info('generate gallery from photos in %s dir' % fromDir)
        xmlData = None
        # FIXME: this '/' may not be portable ...
        albumName = basename(rstrip(fromDir, '/'))
        logger.info('albumName is %s' % albumName)

    up = 'pytof'
    topDir = join(outputDir, up, albumName)
    try:
        if not exists(topDir):
            os.makedirs(topDir)
    except (os.error):
        _err_exit('Cannot create %s' %(topDir))

    print 'output dir is %s' % (topDir)

    try:
        if info:
            print ('\n').join(xmlData.getAlbumList())
        else:
            if fs:
                makefs.main(albumName, topDir, xmlData)
            else:
                makepage.main(albumName, topDir, xmlData, strip_originals, fromDir)

            archive = None
            if Zip or tar:
                archive = mkarchive(fn = join(outputDir, up, albumName),
                                    prefix = join(outputDir, up),
                                    mainDir = albumName,
                                    files = [makepage.cssfile],
                                    Zip = Zip, tar = tar)
                echo('output archive is %s' % (archive))

            if not info and not fs:
                import webbrowser
                webbrowser.open('file://' + join(topDir, 'index.html'))

            if ftp:
                ftpPush(conf, archive, topDir, fs)

    except (KeyboardInterrupt):

        if not info:
            if not fs:
                # os.remove(makepage.cssfile)
                # we should remove the css file if there aren't
                # any other exported albums left... hard to know,
                # may be stored in the rc file, under the Internal section.
                # => if that's the only file in the pytof dir we should be good to go.
                pass

            if exists(topDir):
                rmtree(topDir)

        _err_exit("\nAborted by user")
