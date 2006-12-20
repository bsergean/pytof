#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- python -*-
# $Id$
#
#*****************************************************************************
#
# See LICENSE file for licensing and to see where does some code come from
#
#*****************************************************************************
#
# Main file.
#

__revision__ = '$Id$  (C) 2004 GPL'
__author__ = 'Mathieu Robin'
__dependencies__ = []

from os.path import expanduser
from albumdataparser import AlbumDataParser
import os, sys, getopt
from utils import _err_, _err_exit, help


__version__ = '0.0.1'

class WebPage(object):
    def __init__(self, fileName, title):
        self.fileName = fileName  + ".html"
        self.title = title
        self.code = ''

    def addCode(self, s):
        self.code += s

    def addCodeLine(self, s):
        self.code += s + '\n'

    def getHeader(self):
        return '''
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 TRANSITIONAL//EN">
    <html>
    <head>
    <title>%s</title>
    <link href="../style.css" rel="stylesheet" type="text/css">
    </head>
    <body>''' % self.title

    def getFooter(self):
        return '''
    </body>
    </html>
    '''

    def writePage(self):
        out = file(self.fileName, 'w')
        out.write(self.getHeader())
        out.write(self.code)
        out.write(self.getFooter())
        out.close()

def echo(s):
    sys.stdout.write(s)
    sys.stdout.flush()

def makePhotoPage(photo, linkBack):
    page = WebPage(photo.id, photo.title)
    page.addCodeLine('<div class="square"><a href="%s"><img class="prev" src="%s" /></a></div>'
        % (linkBack, photo.prevPath))
    page.writePage()
    return page.fileName

def main(albumName, libraryPath):
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

def _err_msg(msg):
    sys.stderr.write("%s: %s\n" % (os.path.basename(sys.argv[0]), msg))

def _err_exit(msg):
    sys.stderr.write("%s: %s\n" % (os.path.basename(sys.argv[0]), msg))
    sys.exit(1)

if __name__ == "__main__":

    class BadUsage: pass
    try:
        libraryPath = ''

        # parse args
        if len(sys.argv) < 2:
            _err_msg('missing albumName argument')
            raise BadUsage
        albumName = sys.argv[-1]
        
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
        help(""" 
%s : Export iPhoto library to html

usage : python makepage.py <options> AlbumName
OPTIONS | -l <dir> : iPhoto library path
        | -v : display pytof version
        | -h : display this text
        """,
                       __revision__,
                       __dependencies__,
                       __author__)
