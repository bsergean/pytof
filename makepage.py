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
from albumdataparser import AlbumDataParser, AlbumDataParserError
import os, sys, getopt
from utils import _err_, _err_exit, help, log


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

def main(albumName, libraryPath, xmlFileName):
    try:
        echo("Parsing AlbumData.xml")
        parser = AlbumDataParser(libraryPath, xmlFileName)
        data = parser.parse()
        photos = data.getPicturesIdFromAlbumName(albumName)
        echo("\t[DONE]\n")
    except(AlbumDataParserError):
        _err_exit("Problem parsing AlbumData.xml")

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
        photo = data.getPhotoFromId(id, libraryPath)
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

if __name__ == "__main__":
    print 'foobar'
    # add unit tests here ?
