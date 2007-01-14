#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- python -*-
#*****************************************************************************
#
# See LICENSE file for licensing and to see where does some code come from
#
#*****************************************************************************
#
# Main file.
#

__revision__ = '$Id$  (C) 2006 GPL'
__author__ = 'Benjamin Sergeant'
__dependencies__ = []

import sys
sys.path.insert(1, '../pytof')

from log import logger, quiet
from os.path import expanduser, join, exists, basename, isabs, walk, isdir
from albumdataparser import AlbumDataParser, AlbumDataParserError
import os, sys
from utils import _err_, _err_exit, echo, GetTmpDir, mkarchive
from config import configHandler
import makepage, makefs
from optparse import OptionParser
from shutil import rmtree
from ftp import ftpUploader, ftpPush
from ftplib import error_perm
from getpass import getuser, unix_getpass
from string import rstrip

# FIXME: (see issue 11)
__version__ = open('../VERSION').read().strip()

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


if __name__ == "__main__":
    # Import Psyco if available
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass

    # parse args
    usage = "usage: python %prog <options>"
    parser = OptionParser(usage=usage)
    
    parser.add_option("-a", "--album", dest="albumName", default='',
                      help="The iPhoto library album to process"),
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
                      action="store_true", dest="strip_originals", default=False,
                      help="Remove the originals from the generated gallery Gallery will be way smaller")
    parser.add_option("-d", "--from-directory", dest="fromDir", default='',
                      help="The directory path for the gallery. Do not interact with iPhoto"),

    options, args = parser.parse_args()
    
    if options.version:
        print 'pytof version %s' % (__version__)
        sys.exit(0)

    if options.info: pass
    elif options.fromDir:
        if not isdir(options.fromDir):
            _err_exit('Not a directory: %s' % options.fromDir)
    elif not options.albumName:
        _err_exit('missing albumName argument')
            
    if not options.verbose:
        quiet()

    main(options.albumName, options.libraryPath,
         options.xmlFileName, options.outputDir,
         options.info, options.fs, options.tar,
         options.Zip, options.ftp, options.strip_originals,
         options.fromDir)

