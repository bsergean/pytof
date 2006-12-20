#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- python -*-
#
#*****************************************************************************
#
# See LICENSE file for licensing and to see where does some code come from
#
#*****************************************************************************
#
# fs
#

__revision__ = '$Id: miscutils.py,v 1.17 2005/04/27 16:24:16 bsergean Exp $  (C) 2004 GPL'
__author__ = 'Benjamin Sergeant'
__dependencies__ = []

from os.path import expanduser
from albumdataparser import AlbumDataParser
import os, sys, getopt
from utils import _err_, _err_exit, help

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

if __name__ == "__main__":
    print 'foobar'
    # add unit tests here ?
