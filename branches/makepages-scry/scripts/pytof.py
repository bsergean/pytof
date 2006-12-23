#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- python -*-
# $Id: makepage.py 42 2006-12-20 19:43:06Z bsergean $
#
#*****************************************************************************
#
# See LICENSE file for licensing and to see where does some code come from
#
#*****************************************************************************
#
# Main file.
#

__revision__ = '$Id: makepage.py 42 2006-12-20 19:43:06Z bsergean $  (C) 2006 GPL'
__author__ = 'Benjamin Sergeant'
__dependencies__ = []

import sys
sys.path.insert(1, '../pytof')

from os.path import expanduser, join, exists
from albumdataparser import AlbumDataParser, AlbumDataParserError
import os, sys
from utils import _err_, _err_exit, help, echo, log
from configFile import getConfDirPath, getConfFilePath, canUseCache
import makepage, makefs
from cPickle import dump, load
from ConfigParser import RawConfigParser
from optparse import OptionParser

# FIXME: (see issue 11)
__version__ = '0.0.1'

def main(albumName, libraryPath, xmlFileName, outputDir, info, fs):
    try:
	# generate the config file
	getConfFilePath()
        echo("Parsing AlbumData.xml")
        parser = AlbumDataParser(libraryPath, xmlFileName)
        xmlFileName = parser.xmlFileName
        # can we use the cached xml content ?

        pickleFilename = join(getConfDirPath(), 'xmlData.pickle')
        log(pickleFilename)

        # try to load our stuff from the cache if the xml wasn't modified
        cached = canUseCache(xmlFileName)

        if cached:
            pickleFd = open(pickleFilename)
            xmlData = load(pickleFd)
            pickleFd.close()
        else:
            xmlData = parser.parse()
            xmlData.libraryPath = libraryPath

        # writing the cached data to a file
        pickleFd = open(pickleFilename, 'w')
        dump(xmlData, pickleFd)
        pickleFd.close()
        
        echo("\t[DONE]\n")
    except(AlbumDataParserError):
        _err_exit("Problem parsing AlbumData.xml")

    topDir = join(outputDir, 'out', albumName)
    try:
        if not exists(topDir):
            os.makedirs(topDir)
    except (os.error):
        _err_exit('Cannot create %s' %(topDir))

    print 'output dir is %s' % (topDir)

    if info:
        print ('\n').join(xmlData.getAlbumList())
    else:
        if fs:
            makefs.main(albumName, topDir, xmlData)
        else:
            makepage.main(albumName, topDir, xmlData)


if __name__ == "__main__":

    try:
        from tempfile import mktemp
        import tempfile # FIXME: is there a way to get tempdir value
        # without import tempfile ?
        # mktemp has to be called once for tempdir to be initalized !!
        mktemp()

        # parse args
        usage = "usage: python %prog <options>"
        parser = OptionParser(usage=usage)
        
        parser.add_option("-i", "--info",
                          action="store_true", dest="info", default=False,
                          help="Print info about the collection [default = %default]")
        parser.add_option("-f", "--file-system",
                          action="store_true", dest="fs", default=False,
                          help="Extract album photo to a dir and stop")
        parser.add_option("-V", "--version",
                          action="store_true", dest="version", default=False,
                          help="display version")
        parser.add_option("-l", "--library", dest="libraryPath", default='',
                          help="The iPhoto library directory path"),
        parser.add_option("-x", "--xml-file", dest="xmlFileName", default='',
                          help="The iPhoto library XML file name"),
        parser.add_option("-a", "--album", dest="albumName", default='',
                          help="The iPhoto library album to process"),
        parser.add_option("-o", "--output", dest="outputDir", default=tempfile.tempdir,
                          help="The output directory"),

        options, args = parser.parse_args()

        if options.version:
            print 'pytof version %s' % (__version__)
            
        if not options.albumName and not options.info:
            _err_exit('missing albumName argument')

        main(options.albumName, options.libraryPath,
             options.xmlFileName, options.outputDir,
             options.info, options.fs)

    except (KeyboardInterrupt):
        _err_exit("\nAborted by user")
