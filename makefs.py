#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- python -*-
# $Id: makepage.py 36 2006-12-20 15:53:26Z bsergean $
#
#*****************************************************************************
#
# See LICENSE file for licensing and to see where does some code come from
#
#*****************************************************************************
#
# Main file.
#

from os.path import expanduser
from albumdataparser import AlbumDataParser
import os, sys

__version__ = '0.0.1'

def echo(s):
    sys.stdout.write(s)
    sys.stdout.flush()

def main(albumNamei, libraryPath):
    echo("Parsing AlbumData.xml")
    if not libraryPath: libraryPath = expanduser('~/Pictures/iPhoto Library')
    xmlFileName=os.path.join(libraryPath, 'AlbumData.xml')
    parser = AlbumDataParser(xmlFileName)
    data = parser.parse()
    photos = data.getPicturesIdFromAlbumName(albumName)
    echo("\t[DONE]\n")

    outputPath = 'out'
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)

    dirs = ['photos', 'preview', 'thumbs']
    os.chdir(outputPath)
    if not os.path.exists(albumName):
	os.makedirs(albumName)
        os.chdir(albumName)
        for dir in dirs:
            if not os.path.exists(dir): 
		os.mkdir(dir)

    picsPerPage = 6 ** 2
    pageCounter = 1
    curPage = WebPage("page%2d" % pageCounter, albumName)
    curPage.addCode("<div class=\"square\">")
    
    echo("Writing pictures 00%")
    c = 0
    for id in photos:
        photo = data.getPhotoFromId(id)
        photo.saveCopy(dirs[0])
        photo.makePreview(dirs[1], 640)
        photo.makeThumbnail(dirs[2])
        photoPageName = makePhotoPage(photo, curPage.fileName)
        curPage.addCode("<a href=\"%s\"><img src=\"%s\" class=\"thumb\"/></a>" %
                        (photoPageName, photo.thumbPath))
        c += 1
        if c % picsPerPage == 0 and c < len(photos):
            curPage.addCode("</div>")
            curPage.writePage()
            pageCounter += 1
            curPage = WebPage("page%2d" % pageCounter, albumName)
            curPage.addCode("<div class=\"square\">")
            
        echo("\b\b\b%2d%%" % ((100 * c) / len(photos)))

    echo("\b\b\b\b\tDONE\n")
    curPage.addCode("</div>")
    curPage.writePage()

def _err_exit(msg):
    sys.stderr.write("%s: %s\n" % (os.path.basename(sys.argv[0]), msg))
    sys.exit(1)

if __name__ == "__main__":

    class BadUsage: pass
    try:
        libraryPath = ''
    
        # parse args
        albumName = sys.argv[-1]
        
        import getopt
        opts, args = getopt.getopt(sys.argv[1:], 'Vhl:')

        for opt, val in opts:
            if opt == '-h':
                raise BadUsage
            if opt == '-V':
                print 'pytof version %s' % (__version__)
                sys.exit(0)                             
            elif opt == '-l':
                libraryPath = val
                # ... how to get a parameter
            else:
                raise BadUsage
       
        main(albumName, libraryPath)

    except (KeyboardInterrupt):
        _err_exit("Aborted by user")

    except (getopt.error, BadUsage):
        print """ 
makepage.py : Export iPhoto library to html pages
usage : python makepage.py <options> AlbumName
OPTIONS | -l <dir> : iPhoto library path
        | -v : display pytof version
        | -h : display this text

OTHERS
        
DEPENDENCIES
        PIL, libjpeg, Cocaine

HISTORY
        Mathieu made this program a while ago, and put it in sourceforge
        a while after. Benjamin got rid of the CVS error messages, and put
        it on google code.
"""
