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

from log import logger
from os.path import join, exists, basename, sep
from albumdataparser import AlbumDataParser, AlbumDataParserError
import os, sys
from utils import _err_exit, echo, mkarchive
from config import configHandler
import makepage, makefs
from shutil import rmtree
from ftp import ftpPush
from string import rstrip


class Pytof(object):

    def __init__(self, po, progress):
        self.albumName = po.options.albumName
        self.libraryPath = po.options.libraryPath
        self.xmlFileName = po.options.xmlFileName
        self.outputDir = po.options.outputDir
        self.info = po.options.info
        self.fs = po.options.fs
        self.tar = po.options.tar
        self.Zip = po.options.Zip
        self.ftp = po.options.ftp
        self.stripOriginals = po.options.stripOriginals
        self.fromDir = po.options.fromDir
        self.style = po.options.style

        self.progress = progress
        
    def main(self):
        # init the config file
        conf = configHandler()
        if not conf.ok:
            _err_exit('Problem with the config file')

        libraryPath, xmlFileName, outputDir = \
                     conf.getValuesAndUpdateFromUser(self.libraryPath,
                                                     self.xmlFileName,
                                                     self.outputDir)

        ##
        # get iPhoto datas or flat dir pictures list
        if not self.fromDir:
            try:
                adp = AlbumDataParser(libraryPath, xmlFileName)
                xmlData = adp.maybeLoadFromXML(conf)
            except(AlbumDataParserError):
                _err_exit("Problem parsing AlbumData.xml")
        else:
            logger.info('generate gallery from photos in %s dir' % self.fromDir)
            xmlData = None
            # FIXME: this '/' may not be portable ...
            self.albumName = basename(rstrip(self.fromDir, '/'))
            logger.info('albumName is %s' % self.albumName)

	# FIXME: remove the output dir if a problem occur
        up = 'pytof'
        topDir = join(self.outputDir, up, self.albumName)
        try:
            if not exists(topDir):
                os.makedirs(topDir)
        except (os.error):
            _err_exit('Cannot create %s' %(topDir))

        echo('output dir is %s' % (topDir))

        try:
            if self.info:
                for a in xmlData.getAlbumList():
                    print a.encode('utf8')
            else:
                if self.fs:
                    makefs.main(self.albumName, topDir, xmlData)
                else:
                    makepage.main(self.albumName, topDir, xmlData,
                                  self.stripOriginals, self.style,
                                  self.fromDir, self.progress)

            archive = None
            if self.Zip or self.tar:
                archive = mkarchive(fn = join(outputDir, up, self.albumName),
                                    prefix = join(outputDir, up),
                                    mainDir = self.albumName,
                                    files = [],
                                    Zip = self.Zip,
                                    tar = self.tar)
                echo('output archive is %s' % (archive))

            if not self.info and not self.fs:
                import webbrowser
                url = 'file:///'
                url += '/'.join(topDir.split(sep)) + '/'
                url += '/'.join(['..', 'index.html'])
                webbrowser.open(url)

            if self.ftp:
                ftpPush(conf, archive, topDir, self.fs)

        except (KeyboardInterrupt):

            if not self.info:
                if not self.fs:
                    # os.remove(makepage.cssfile)
                    # we should remove the css file if there aren't
                    # any other exported albums left... hard to know,
                    # may be stored in the rc file, under the Internal section.
                    # => if that's the only file in the pytof dir we should be good to go.
                    pass

                if exists(topDir):
                    rmtree(topDir)

                _err_exit("\nAborted by user")

