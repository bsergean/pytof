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
<link href="/home/bsergean/src/pytof/branches/makepages-scry/share/scry.css" rel="stylesheet" type="text/css">
</head>
<body>
<table cellpadding="5" cellspacing="0" width="85%%" border="0" align="center">
  <tr>
    <td id="t_main" width="100%%" colspan="2">
      <div class="images">
''' % self.title

    def getFooter(self):
        return '''
      </div>
    </td>
  </tr>
  
  <tr>
    <td align="left"></td>
    <td align="right"></td>
  </tr>
</table>
       
</body>
</html>
'''

    def writePage(self):
        out = file(self.fileName, 'w')
        out.write(self.getHeader())
        out.write(self.code)
        out.write(self.getFooter())
        out.close()

# http://docs.python.org/tut/node11.html
class PhotoWebPage(WebPage):
    
    def __init__(self, fileName, title, home):
        WebPage.__init__(self, fileName, title)

        # home is `basename home` instead
        self.home = os.path.basename(home)
    
    def getHeader(self):
        return '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 TRANSITIONAL//EN">
<html>
<head>
<title>%s</title>
<link href="/home/bsergean/src/pytof/branches/makepages-scry/share/scry.css" rel="stylesheet" type="text/css">
</head>
<body>

<table cellpadding="5" cellspacing="0" width="85%%" border="0" align="center">
  <tr>
    <td align="left">
 <a href="%s">home</a> </td>
  </tr>
</table>


<table cellpadding="5" cellspacing="0" width="85%%" border="0" align="center">
  <tr>
    <td id="t_main" width="100%%" colspan="2">
      <div class="images">
''' % (self.title, self.home)

    def getFooter(self):
        return '''
      </div>
    </td>
  </tr>
  
  <tr>
    <td align="left"></td>
    <td align="right"></td>
  </tr>
</table>
       
</body>
</html>
'''

    def addSkeleton(self, photo, original):
        self.addCodeLine(
            '''
            
     <table align="center" cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td width="100%%" colspan="3" align="center">
            <div class="images">

            <img src="%s" alt="img_0912.jpg" />
            <br />
            FIXME: photo_name.jpg here:
            <br />
            <a href="%s">Original picture: FIXME: Dimensions, FIXME: Size KB</a>
            </div>
          </td>
        </tr>

        <tr>

          <td width="30%%" align="left" valign="bottom">
            <div class="images">
<a style="text-decoration: none;" href="prev.jpg"><img src="prev.jpg" alt="previous" /><br />&lt; previous</a>            </div>
          </td>
          <td width="40%%" align="middle" valign="bottom">

            <p> FIXME: here we should put the photo metadata
            </p>

          </td>
          <td width="30%%" align="right" valign="bottom">
            <div class="images">
<a style="text-decoration: none;" href="next.jpg"><img src="next.jpg" alt="next" /><br />&lt; next</a>            </div>
          </td>
        </tr>
      </table>
      ''' % (photo, original))


def makePhotoPage(photo, linkBack, topDir):
    '''
    Should have a next and back with thumbnails
    '''
    page = PhotoWebPage(join(topDir, photo.id), photo.title, linkBack)
    #page.addCodeLine('<div class="square"><a href="%s"><img class="prev" src="%s" /></a></div>'
    #    % (linkBack, photo.prevPath))

    page.addSkeleton(photo.prevPath,
                     join('photos', photo.id + '.jpg')) # fixme: check extension
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

    cssfile = 'scry.css'
    cssfilename = join('share', cssfile)
    if not exists(cssfilename):
        _err_('No css file was found: HTML files look and feel will be bad')
    else:
        # FIXME: where do we get that install path ...
        copy(cssfilename, join(topDir, cssfile))

    log(topDir)
    
    curPage = WebPage(join(topDir, 'index'), albumName)
    
    sys.stderr.write("Writing pictures\n")
    c = 1
    photos = data.getPicturesIdFromAlbumName(albumName)
    nb_photos = len(photos)
    for id in photos:
        photo = data.getPhotoFromId(id)
        photo.saveCopy(dirs[0])
        photo.makePreview(dirs[1], 640)
        photo.makeThumbnail(dirs[2])
        photoPageName = makePhotoPage(photo, curPage.fileName, topDir)
        curPage.addCode("<a href=\"%s\"><img src=\"%s\" alt=\"toto.jpg\" border=\"0\"/></a>" %
                        (photoPageName, photo.thumbPath))

        # progress
        s = "\r%f %% - (%d processed out of %d) " \
            % (100 * float(c) / float(nb_photos), c, nb_photos)
        sys.stderr.write(s)
        c += 1

    sys.stderr.write('\n')
    curPage.writePage()

if __name__ == "__main__":
    print 'foobar'
    # add unit tests here ?
