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
from os.path import expanduser, join, exists, isdir
import os, sys
from utils import _err_, _err_exit, echo, GetTmpDir
from ConfigParser import RawConfigParser
from shutil import copy
from optparse import OptionParser
from log import quiet
from version import __version__

class pytofOptions(object):

    def __init__(self):
        # parse args
        usage = "usage: python %prog <options>"
        parser = OptionParser(usage=usage)
        
        parser.add_option("-a", "--album", dest="albumName", default='',
                          help="The iPhoto library album to process")
        parser.add_option("-i", "--info",
                      action="store_true", dest="info", default=False,
                          help="Print info about the collection [default = %default]")
        parser.add_option("-o", "--output", dest="outputDir", default=GetTmpDir(),
                          help="The output directory [%default + out/ALBUMNAME]"),
        parser.add_option("-f", "--file-system",
                          action="store_true", dest="fs", default=False,
                          help="Extract album photo to OUTPUTDIR and stop")
        parser.add_option("-t", "--tar-archive",
                          action="store_true", dest="tar", default=False,
                          help="Create a tar archive from the exported datas")
        parser.add_option("-z", "--zip-archive",
                          action="store_true", dest="Zip", default=False,
                          help="Create a tar archive from the exported datas")
        parser.add_option("-V", "--version",
                          action="store_true", dest="version", default=False,
                          help="display version")
        parser.add_option("-v", "--verbose",
                          action="store_true", dest="verbose", default=False,
                          help="Report a number of information")
        parser.add_option("-l", "--library", dest="libraryPath", default='',
                          help="The iPhoto library directory path"),
        parser.add_option("-x", "--xml-file", dest="xmlFileName", default='',
                          help="The iPhoto library XML file name"),
        parser.add_option("-u", "--ftp-upload",
                          action="store_true", dest="ftp", default=False,
                          help="Upload pytof output to a ftp site")
        parser.add_option("-s", "--strip-originals",
                          action="store_true", dest="stripOriginals", default=False,
                          help="Remove the originals from the generated gallery Gallery will be way smaller")
        parser.add_option("-d", "--from-directory", dest="fromDir", default='',
                          help="The directory path for the gallery. Do not interact with iPhoto"),

        self.options, args = parser.parse_args()

    def check(self):
    
        if self.options.version:
            print 'pytof version %s' % (__version__)
            sys.exit(0)

        if self.options.info: pass
        elif self.options.fromDir:
            if not isdir(self.options.fromDir):
                _err_exit('Not a directory: %s' % self.options.fromDir)
        elif not self.options.albumName:
            _err_exit('missing albumName argument')
            
        if not self.options.verbose:
            quiet()


