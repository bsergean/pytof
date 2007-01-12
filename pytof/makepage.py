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

from log import loggers
import logging
# FIXME: find a way to get the file name in python
logger = loggers['makepage']

from os.path import expanduser, join, exists, basename
from albumdataparser import AlbumDataParser, AlbumDataParserError, AlbumDataFromDir
import os, sys
from utils import _err_, _err_exit, echo, ProgressMsg
from shutil import copy

css = 'scry.css'
cssfile = join(os.pardir, 'share', css)

commercial = '''
<table cellpadding="5" cellspacing="0" width="85%%" border="0" align="center">
  <tr>
    <td align="right">
      Powered by <a href="http://code.google.com/p/pytof/">pytof</a>
    </td>
  </tr>
</table 
'''

class WebPage(object):
    def __init__(self, fileName, title):
        self.fileName = fileName  + ".html"
        logger.info(self.fileName)
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
<link href="../scry.css" rel="stylesheet" type="text/css">
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

%s
       
</body>
</html>
''' % commercial

    def writePage(self):
        out = file(self.fileName, 'w')
        out.write(self.getHeader())
        out.write(self.code)
        out.write(self.getFooter())
        out.close()

# http://docs.python.org/tut/node11.html
class PhotoWebPage(WebPage):

    skeleton_template = '''
        <table align="center" cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td width="100%%" colspan="3" align="center">
            <div class="images">

            <img src="%(preview)s" alt="img_0912.jpg" />
            <br />
            %(preview_filename)s
            <br />
            <a href="%(original)s">Original picture: %(width)d x %(height)d, %(size)d KB</a>
            </div>
          </td>
        </tr>

        <tr>

          <td width="30%%" align="left" valign="bottom">
            <div class="images">
<a style="text-decoration: none;" href="%(prev)s"><img src="%(prev_thumb)s" alt="previous" /><br />&lt; previous</a>            </div>
          </td>
          <td width="40%%" align="middle" valign="bottom">

            <p> %(exif_infos)s
            </p>

          </td>
          <td width="30%%" align="right" valign="bottom">
            <div class="images">
<a style="text-decoration: none;" href="%(next)s"><img src="%(next_thumb)s" alt="next" /><br />next &gt; </a>            </div>
          </td>
        </tr>
        </table>
'''

    skeleton_template_originals_stripped = '''
        <table align="center" cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td width="100%%" colspan="3" align="center">
            <div class="images">

            <img src="%(preview)s" alt="img_0912.jpg" />
            <br />
            %(preview_filename)s
            </div>
          </td>
        </tr>

        <tr>

          <td width="30%%" align="left" valign="bottom">
            <div class="images">
<a style="text-decoration: none;" href="%(prev)s"><img src="%(prev_thumb)s" alt="previous" /><br />&lt; previous</a>            </div>
          </td>
          <td width="40%%" align="middle" valign="bottom">

            <p> %(exif_infos)s
            </p>

          </td>
          <td width="30%%" align="right" valign="bottom">
            <div class="images">
<a style="text-decoration: none;" href="%(next)s"><img src="%(next_thumb)s" alt="next" /><br />next &gt; </a>            </div>
          </td>
        </tr>
        </table>
'''

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
<link href="../scry.css" rel="stylesheet" type="text/css">
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

%s
  
</table>
       
</body>
</html>
''' % commercial

    def addSkeleton(self, dico, strip_originals):
        template = self.skeleton_template
        if strip_originals:
            template = self.skeleton_template_originals_stripped
            
        self.addCodeLine(template % dico)

def makePhotoPage(photo, linkBack, topDir, prev, next, strip_originals):
        '''
        Should have a next and back with thumbnails
        '''
        page = PhotoWebPage(join(topDir, photo.id), photo.title, linkBack)
        #page.addCodeLine('<div class="square"><a href="%s"><img class="prev" src="%s" /></a></div>'
        #    % (linkBack, photo.prevPath))

        dico = {}
        dico['width'] = photo.width
        dico['height'] = photo.height
        dico['size'] = photo.sizeKB
        dico['exif_infos'] = ('</br>').join(photo.exif_infos)
        dico['preview'] = join('preview', 'pv_' + photo.id + photo.getFileType())
        dico['preview_filename'] = basename(dico['preview'])
        dico['original'] = join('photos', photo.id + photo.getFileType())
        dico['prev'] = prev.id + '.html'
        dico['prev_thumb'] = join('thumbs',   'th_' + prev.id + prev.getFileType())
        dico['next'] = next.id + '.html'
        dico['next_thumb'] = join('thumbs',   'th_' + next.id + next.getFileType())

        page.addSkeleton(dico, strip_originals)
        page.writePage()
        return page.fileName

def main(albumName, topDir, xmlData, strip_originals, fromDir):
    logger.setLevel(logging.INFO)
    logger.info('strip_originals = %s' % strip_originals)

    data = xmlData
    if fromDir:
        data = AlbumDataFromDir(fromDir)

    leafDirs = ['photos', 'preview', 'thumbs']
    dirs = []
    for leafDir in leafDirs:
        Dir = join(topDir, leafDir)
        dirs.append(Dir)
        if not os.path.exists(Dir):
            try:
                os.makedirs(Dir)
            except (os.error):
                _err_exit('Cannot create %s' %(Dir))

    # FIXME: how do we get the package install path, to retrieve
    # the resource dir next ...quick hack for now
    logger.info(cssfile)
    if not exists(cssfile):
        _err_('No css file was found: HTML files look and feel will be bad')
    else:
        copy(cssfile, join(topDir, os.pardir, css))

    logger.info(topDir)
    
    curPage = WebPage(join(topDir, 'index'), albumName)
    
    logger.info("Writing pictures\n")
    
    photos = data.getPicturesIdFromAlbumName(albumName)
    progress = ProgressMsg(len(photos), sys.stderr)                           
    for i in xrange(len(photos)):

        pic_id = photos[i]
        logger.debug('processing photo %s' % pic_id)
        
        photo = data.getPhotoFromId(pic_id)
        prev = data.getPhotoFromId(photos[i-1])
        try:
            next = data.getPhotoFromId(photos[i+1])
        except (IndexError):
            # ok I know it's crappy programming :)
            next = data.getPhotoFromId(photos[0])

        if not strip_originals:
            photo.saveCopy(dirs[0])
        photo.makePreview(dirs[1], 640)
        photo.makeThumbnail(dirs[2])

        # FIXME: makePhotoPage return photoPageName which shoule be
        # modified to HTML/123.html. We would only have to create
        # a dir HTML, change the links in the index to HTML/123.html
        # and create the per page file in HTML/123.html
        makePhotoPage(photo, curPage.fileName, topDir,
                      prev, next, strip_originals)
        curPage.addCode("<a href=\"%s\"><img src=\"%s\" alt=\"toto.jpg\" border=\"0\"/></a>" %
                        (photo.id + '.html',
                         join('thumbs', 'th_' + photo.id + photo.getFileType())))
        progress.Increment()
        
    curPage.writePage()
