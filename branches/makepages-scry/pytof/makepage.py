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

__revision__ = '$Id$  (C) 2006 GPL'
__author__ = 'Mathieu Robin'
__dependencies__ = []

from os.path import expanduser, join, exists
from albumdataparser import AlbumDataParser, AlbumDataParserError
import os, sys, getopt
from utils import _err_, _err_exit, help, log, echo
from shutil import copy

__version__ = '0.0.1'

class WebPage(object):
    def __init__(self, fileName, title):
        self.fileName = fileName  + ".html"
        log(self.fileName)
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

def makePhotoPage(photo, linkBack, topDir):
    page = WebPage(join(topDir, photo.id), photo.title)
    page.addCodeLine('<div class="square"><a href="%s"><img class="prev" src="%s" /></a></div>'
        % (linkBack, photo.prevPath))
    page.writePage()
    return page.fileName

def main(albumName, topDir, xmlData):

    data = xmlData

    leafDirs = ['photos', 'preview', 'thumbs']
    dirs = []
    for leafDir in leafDirs:
        Dir = join(topDir, leafDir)
        dirs.append(Dir)
        if not os.path.exists(Dir):
            try:
                os.makedirs(Dir)
            except (error):
                _err_exit('Cannot create %s' %(Dir))

    # FIXME: share will be in the pytof home dir
    cssfile = 'style.css'
    cssfilename = join('share', cssfile)
    if not exists(cssfilename):
        _err_('No css file was found: HTML files look and feel will be bad')
    else:
        # FIXME: where do we get that install path ...
        copy(cssfilename, join(topDir, cssfile))

    picsPerPage = 6 ** 2
    pageCounter = 1

    log(topDir)
    
    curPage = WebPage(join(topDir, "page%2d" % pageCounter), albumName)
    curPage.addCode("<div class=\"square\">")
    
    echo("Writing pictures 00%")
    c = 0
    photos = data.getPicturesIdFromAlbumName(albumName)
    for id in photos:
        photo = data.getPhotoFromId(id)
        photo.saveCopy(dirs[0])
        photo.makePreview(dirs[1], 640)
        photo.makeThumbnail(dirs[2])
        photoPageName = makePhotoPage(photo, curPage.fileName, topDir)
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

    echo("\b\b\b\b\t[DONE]\n")
    curPage.addCode("</div>")
    curPage.writePage()

if __name__ == "__main__":
    print 'foobar'
    # add unit tests here ?
