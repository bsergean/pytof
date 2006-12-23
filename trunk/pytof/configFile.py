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

from os.path import expanduser, join, exists
import os, sys, getopt
from utils import _err_, _err_exit, help, echo, log
from ConfigParser import RawConfigParser

def getConfDirPath():
    # Creating conf dir
    try:
        confDir = join(os.environ["HOME"],'.pytof')
        if not exists(confDir):
            os.makedirs(confDir)
        return confDir
    except(os.error):
        _err_exit('Cannot create %s' %(confDir))

def getConfFilePath():
    # Creating conf dir

    confFilename = join(getConfDirPath(), 'pytof.ini')

    exist = exists(confFilename)
    if exist:
        size = os.stat(confFilename).st_blocks

    if not exist or size == 0:
        # create it
        log('Create brand new config file')
        confFd = open(confFilename, 'w')
        content = '''
[Internals]
xmlTimestamp=0
'''
        confFd.write(content)
        confFd.close()

    return confFilename

def printConfFile():
    # Creating conf dir

    confFilename = join(getConfDirPath(), 'pytof.ini')

    exist = exists(confFilename)
    if not exist:
        print 'No such file'
    else:
        size = os.stat(confFilename).st_blocks
        if size == 0:
            print '(Empty file)'
        else:
            for l in open(confFilename):
                print l

def canUseCache(xmlFileName):

    cache = False
    config = RawConfigParser()
    config.read(getConfFilePath())
    if config.has_option('Internals', 'xmlTimestamp'):
        xmlTimestamp = config.get('Internals', 'xmlTimestamp')
        statinfo = os.stat(xmlFileName).st_mtime
        if statinfo == int(xmlTimestamp):
            log('Caching')
            cache = True
        else:
            log('Not caching')
            configFD = open(getConfFilePath(), 'w')
            config.set('Internals', 'xmlTimestamp', statinfo)
            config.write(configFD)
            configFD.close()

    return cache
