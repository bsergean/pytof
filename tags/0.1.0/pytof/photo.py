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

__revision__ = '$Id$  (C) 2004 GPL'
__author__ = 'Mathieu Robin'
__dependencies__ = ['Image']

from os.path import join, getsize, basename
from shutil import copy
import sys, os, time
from utils import TryToImport, log
from EXIF import process_file

TryToImport(__dependencies__)
for mod in __dependencies__:
    exec 'import ' + mod

def EXIF_tags(fn):
    # FIXME: strip some keys for speed-up instead of
    # returning the whole list of tags
    # see EXIF notes
    # if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename',
    #                        'EXIF MakerNote'):
    # after some timing test there's no speedup ... kept for reference
    # it may be faster to hook a new method in EXIF to just lookup some values
    #
    # We should do a better timing with the timeit module (in EXIFTest.py
    #
    f = open(fn, 'rb')
    tags = process_file(f)
    for t in ['JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote']:
        if tags.has_key(t):
            del tags[t]
    f.close()
    return tags

def EXIF_infos(fn):
    tags = EXIF_tags(fn)
    infos = []
    infos.append('Model: %s' % str(tags.get('Image Model', 'Unknown')))
    infos.append('Date: %s' % tags.get('EXIF DateTimeOriginal', 'Unknown'))
    infos.append('Flash: %s' % tags.get('EXIF Flash', 'Unknown'))
    return infos


class Photo(object):
    def __init__(self, fileName, id=None, title='', comment='', date=''):
        self.image = Image.open(fileName)
        self.fileName = fileName
        if id == None:
            self.id = time.strftime("%y%j%H%M%S")
        else:
            self.id = id
        self.title = title
        self.comment = comment
        self.imagePath = None
        self.thumbPath = None
        self.prevPath = None

        self.width = self.image.size[0]
        self.height = self.image.size[1]
        self.sizeKB = getsize(self.fileName) / 1024
        self.exif_infos = EXIF_infos(self.fileName)

    def getBaseName(self):
        return str(self.id)

    def getFileType(self):
        return basename(self.fileName).split('.')[-1].lower()

    def saveCopy(self, path):
        log(path)
        self.imagePath = join(path, self.getBaseName() + '.'
                              + self.getFileType())
        copy(self.fileName, self.imagePath)

    def makeThumbnail(self, path, size=100):
        width = self.image.size[0]
        height = self.image.size[1]
        if width > height:
            xOffset = (width - height) / 2
            yOffset = 0
            cropLength = height
        else:
            xOffset = 0
            yOffset = (height - width) / 2
            cropLength = width
        thumb = self.image.crop((xOffset,
                                 yOffset,
                                 width - xOffset,
                                 height - yOffset))
        thumb = thumb.resize((size, size), Image.ANTIALIAS)
        self.thumbPath = os.path.join(path, 'th_' + self.getBaseName() + '.jpg')
        thumb.save(self.thumbPath, quality=80)

    def makePreview(self, path, maxDim=800):
        width = self.image.size[0]
        height = self.image.size[1]
        if width > height and width > maxDim:
            newWidth = maxDim
            newHeight = int(maxDim * float(height) / width)
        elif height > width and height > maxDim:
            newWidth = int(maxDim * float(width) / height)
            newHeight = maxDim
        else:
            newWidth = 0
            newHeight = 0
        if (newWidth, newHeight) != (0, 0):
            out = self.image.resize((newWidth, newHeight), Image.ANTIALIAS)
        else:
            out = self.image
        self.prevPath = os.path.join(path, 'pv_' + self.getBaseName() + '.jpg')
        out.save(self.prevPath, quality=95)


if __name__ == '__main__':
    photo = Photo(sys.argv[1])
    photo.makeThumbnail('thumbs')
    photo.makePreview('previews')
