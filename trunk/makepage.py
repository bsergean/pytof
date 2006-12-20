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

from albumdataparser import AlbumDataParser
import os, sys


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

def main():
    echo("Parsing AlbumData.xml")
    albumName = sys.argv[1]
    parser = AlbumDataParser()
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

        # parse args
        import getopt
        opts, args = getopt.getopt(sys.argv[1:], 'hfid:e:')

        for opt, val in opts:
            if opt == '-h':
                raise BadUsage
            elif opt == '-d':
                dir = val
                s = "Usefull to know how to grab a dir : %s\n" %(dir)
            else:
                raise BadUsage
       
        main()

    except (KeyboardInterrupt):
        _err_exit("Aborted by user")

    except (getopt.error, BadUsage):
        print """ 
makepage.py : Export iPhoto library to html pages
usage : python makepage.py <options> AlbumName
OPTIONS | -d <dir> : FIXME does nothing
        | -h : display this text

OTHERS
        
DEPENDENCIES
        PIL, libjpeg, Cocaine

HISTORY
        Mathieu made this program a while ago, and put it in sourceforge
        a while after. Benjamin got rid of the CVS error messages, and put
        it on google code.
"""
