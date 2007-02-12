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
from os.path import expanduser, join, exists, getsize
import os, sys
from utils import _err_, _err_exit, echo, GetTmpDir
from ConfigParser import RawConfigParser
from shutil import copy

class configHandler:

    template = '''
[library]

[Internals]
xmlTimestamp=0

[ftp]
'''

    def __init__(self, confDir=None):

        self.ok = False

        try:
            if confDir == None:
                confDir = join(expanduser('~'),'.pytof')
            if not exists(confDir):
                os.makedirs(confDir)
            self.confDir = confDir
        except(os.error):
            _err_exit('Cannot create %s' %(confDir))
            return

        # from now on, it should be safe as we were able to
        # create the main dir
        confFilename = join(self.confDir, 'pytof.ini')

        exist = exists(confFilename)
        if exist:
            size = getsize(confFilename)

        if not exist or size == 0:
            # create it
            logger.info('Create brand new config file')
            # FIXME: this file may contains password, it has to be
            # created in 600 mode (os.chmod ?)
            confFd = open(confFilename, 'w')
            confFd.write(self.template)
            confFd.close()

        self.confFilename = confFilename

        self.pickleFilename = join(self.confDir, 'xmlData.pickle')
        logger.info(self.pickleFilename)
        self.Load()
        self.ok = True

    def Load(self):
        self.config = RawConfigParser()
        self.config.read(self.confFilename)

    def Open(self):
        ''' Need to Open and Write when serializing '''
        self.configFD = open(self.confFilename, 'w')

    def Close(self):
        ''' Need to Open and Write when serializing '''
        self.config.write(self.configFD)
        self.configFD.close()

    def Print(self):
        ''' Print the config file on stdout '''
        if not self.ok: return # FIXME: add error message
        if os.name == 'posix' or os.name == 'mac':
            copy(self.confFilename, '/dev/stdout')

    # library path
    def hasLibraryPath(self):
        return self.config.has_option('library', 'libraryPath')

    def getLibraryPath(self):
        return self.config.get('library', 'libraryPath')

    def setLibraryPath(self, libraryPath):
        # we have to create a ftp section ...
        logger.debug('setLibraryPath')
        self.Open()
        section = 'library'
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, 'libraryPath', libraryPath)
        self.Close()

    # xml filename
    def hasXmlFileName(self):
        return self.config.has_option('library', 'xmlFileName')

    def getXmlFileName(self):
        return self.config.get('library', 'xmlFileName')

    def setXmlFileName(self, xmlFileName):
        # we have to create a ftp section ...
        logger.debug('setXmlFileName')
        self.Open()
        section = 'library'
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, 'xmlFileName', xmlFileName)
        self.Close()

    # output directory
    def hasOutputDir(self):
        return self.config.has_option('library', 'outputDir')

    def getOutputDir(self):
        return self.config.get('library', 'outputDir')

    def setOutputDir(self, outputDir):
        # we have to create a ftp section ...
        logger.debug('setOutputDir')
        self.Open()
        self.config.set('library', 'outputDir', outputDir)
        self.Close()

    # ftp params
    def hasFtpParams(self):
        return self.config.has_option('ftp', 'host') and \
               self.config.has_option('ftp', 'user') and \
               self.config.has_option('ftp', 'passwd') and \
               self.config.has_option('ftp', 'remoteDir')

    def getFtpParams(self):
        return self.config.get('ftp', 'host'), \
               self.config.get('ftp', 'user'), \
               self.config.get('ftp', 'passwd'), \
               self.config.get('ftp', 'remoteDir')

    def setFtpParams(self, host, user, passwd, remoteDir):
        # we have to create a ftp section ...
        logger.debug('setFtpParams')
        self.Open()        
        self.config.set('ftp', 'host', host)
        self.config.set('ftp', 'user', user)
        self.config.set('ftp', 'passwd', passwd)
        self.config.set('ftp', 'remoteDir', remoteDir)
        self.Close()

    def canUseCache(self, xmlFileName):
        if not self.ok: return False

        # is there a cache file ?
        if not exists(self.pickleFilename):
            return False

        cache = False
        if self.config.has_option('Internals', 'xmlTimestamp'):
            xmlTimestamp = self.config.get('Internals', 'xmlTimestamp')
            statinfo = os.stat(xmlFileName).st_mtime
            if statinfo == int(xmlTimestamp):
                logger.info('Caching')
                cache = True
            else:
                logger.info('Not caching')
                self.Open()
                self.config.set('Internals', 'xmlTimestamp', statinfo)
                self.Close()

        return cache

    def getValuesAndUpdateFromUser(self, libraryPath, xmlFileName, outputDir):
        # config file parameters
        if self.hasLibraryPath() and not libraryPath:
            libraryPath = self.getLibraryPath()
        else:
            self.setLibraryPath(libraryPath)
            
        if self.hasXmlFileName() and not xmlFileName:
            xmlFileName = self.getXmlFileName()
        else:
            self.setXmlFileName(xmlFileName)

        if outputDir == GetTmpDir():
            if self.hasOutputDir():
                outputDir = self.getOutputDir()
        else:
            self.setOutputDir(outputDir)

        return libraryPath, xmlFileName, outputDir
