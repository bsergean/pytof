#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- python -*-
#
#*****************************************************************************
#
# See LICENSE file for licensing and to see where does some code come from
#
#*****************************************************************************

__revision__ = '$Id: utils.py 67 2006-12-22 22:53:55Z bsergean $  (C) 2004 GPL'
__author__ = 'Benjamin Sergeant'

from log import loggers
# FIXME: find a way to get the file name in python
logger = loggers['configFile']

from os.path import expanduser, join, exists
import os, sys, getopt
from utils import _err_, _err_exit, help, echo, log
from ConfigParser import RawConfigParser

class configHandler:

    template = '''
[Internals]
xmlTimestamp=0

[ftp]
'''

    def __init__(self):

        self.ok = False

        try:
            # FIXME: should use ~ char instead
            confDir = join(os.environ["HOME"],'.pytof')
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
            size = os.stat(confFilename).st_blocks

        if not exist or size == 0:
            # create it
            log('Create brand new config file')
            # FIXME: this file may contains password, it has to be
            # created in 600 mode (os.chmod ?)
            confFd = open(confFilename, 'w')
            confFd.write(self.template)
            confFd.close()

        self.confFilename = confFilename

        self.pickleFilename = join(self.confDir, 'xmlData.pickle')
        log(self.pickleFilename)

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
        for l in open(confFilename):
            print l

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

        cache = False
        if self.config.has_option('Internals', 'xmlTimestamp'):
            xmlTimestamp = self.config.get('Internals', 'xmlTimestamp')
            statinfo = os.stat(xmlFileName).st_mtime
            if statinfo == int(xmlTimestamp):
                log('Caching')
                cache = True
            else:
                log('Not caching')
                self.Open()
                self.config.set('Internals', 'xmlTimestamp', statinfo)
                self.Close()

        return cache
