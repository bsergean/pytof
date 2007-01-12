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

from config import configHandler
from os import remove
from unittest import TestCase
from shutil import copy, copytree, rmtree
from tempfile import mkdtemp, mktemp
from os.path import join, basename
from albumdataparser import AlbumDataParser
from timeit import Timer

from log import MainLogger, loggers
logger = loggers['ftp_test']

# comment me if you want to debug here
MainLogger.quiet()

class TestConfigHandler(TestCase):

    def setUp(self):
        self.tempdir = mkdtemp()

#    def tearDown(self):
#        rmtree(self.tempdir)

    def testInit(self):
        '''
        The config file should be called pytof.ini,
        and be located inside the config dir
        '''
        conf = configHandler('data/conf')
        self.assertEquals("data/conf/pytof.ini", conf.confFilename)

    def _InitAndSetLibrarySection(self):
        '''
        As we do some real stuff with the config file we
        should work on a copy.
        '''
        tget = join(self.tempdir, 'data')
        copytree('data', tget)

        self.xmlFilename = 'AlbumData_gnocchi.xml'
        self.libraryPath = tget
        
        self.conf = configHandler(join(tget,'conf'))

        self.conf.setLibraryPath(self.libraryPath)
        self.conf.setXmlFileName(self.xmlFilename)

        self.assertEquals(self.conf.getLibraryPath(), self.libraryPath)
        self.assertEquals(self.conf.getXmlFileName(), self.xmlFilename)        

    def testInitAndSetLibrarySection(self):
        self._InitAndSetLibrarySection()
    
    def _InitFromXml(self):
        self._InitAndSetLibrarySection()

        self.adp = AlbumDataParser(self.libraryPath, self.xmlFilename)
        self.adp.maybeLoadFromXML(self.conf)

    def testInitFromXml(self):
        self._InitFromXml()

    def testTwoInitFromXml(self):
        '''
        Check that two consecutive loads works even
        if we delete the pickled file
        '''        
        self._InitFromXml()

        # destroy the pickle file name and try to reload.
        remove(self.conf.pickleFilename)
        self.adp.maybeLoadFromXML(self.conf)

    def testTwoInitFromXmlWithNewObject(self):
        '''
        Check that two consecutive loads works even
        if we delete the pickled file, and create a new object
        '''
        self._InitFromXml()
        
        # destroy the pickle file name and try to reload.
        remove(self.conf.pickleFilename)
        adp = AlbumDataParser(self.libraryPath, self.xmlFilename)
        adp.maybeLoadFromXML(self.conf)

    
    # TODO: Write a more complex pytof.ini file to test everything
    # Not tested yet: ftp params
