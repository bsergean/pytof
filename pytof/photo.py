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

__revision__ = '$Id$  (C) 2006 GPL'
__author__ = 'Mathieu Robin'

from log import logger
from os.path import join, getsize, basename, splitext
from shutil import copy
import sys, os, time
from utils import TryToImport
from exif import process_file

try:
    import Image
except ImportError:
    try:
        import wxpil as Image
    except ImportError:
        logger.error('No Image processing module available. Install wxPython or PIL.')
        sys.exit(0)

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
        self.rotation = None

        self.width = self.image.size[0]
        self.height = self.image.size[1]
        self.sizeKB = getsize(self.fileName) / 1024
        self.exif_infos = self.EXIF_infos()
        self.date = date

    def EXIF_infos(self):
        try:
            tags = EXIF_tags(self.fileName)
        except:
            logger.error('%s: EXIF extraction failed' % self.fileName)
            tags = {}
        self.rotation = str(tags.get('Image Orientation', 'Unknown'))

	class _datablob:
	    def __init__(self, **args):
		self.__dict__.update(args)

        infos = _datablob()
        infos.model = str(tags.get('Image Model', 'Unknown'))
        infos.date = str(tags.get('EXIF DateTimeOriginal', 'Unknown'))
        infos.flash = str(tags.get('EXIF Flash', 'Unknown'))

        return infos

    def getBaseName(self):
        return str(self.id)

    def getFileType(self):
        return splitext(self.fileName)[1].lower()

    def saveCopy(self, path):
        logger.info(path)
        self.imagePath = join(path, self.getBaseName()
                              + self.getFileType())
        copy(self.fileName, self.imagePath)

    def makeThumbnail(self, path, size=100):
        ''' Thumb can be created to a relative path '''
        width = self.image.size[0]
        height = self.image.size[1]
        if width > height:
            xOffset = (width - height) / 2
            yOffset = 0
            #not used: cropLength = height
        else:
            xOffset = 0
            yOffset = (height - width) / 2
            #not used: cropLength = width
        thumb = self.image.crop((xOffset,
                                 yOffset,
                                 width - xOffset,
                                 height - yOffset))
        thumb = thumb.resize((size, size), Image.ANTIALIAS)

        if self.rotation == 'Rotated 90 CW':
            logger.debug('makeThumbnail: Rotate')
            thumb = thumb.rotate(-90)
        else:
            logger.debug('makeThumbnail: Do not rotate')
        
        self.thumbPath = os.path.join(path, 'th_' + self.getBaseName() + self.getFileType())
        logger.debug('thumb will be %s', self.thumbPath)
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

        if self.rotation == 'Rotated 90 CW':
            logger.debug('makePreview: Rotate')
            out = out.rotate(-90)
        else:
            logger.debug('makePreview: Do not rotate')
            
        self.prevPath = os.path.join(path, 'pv_' + self.getBaseName() + self.getFileType())
        out.save(self.prevPath, quality=95)


if __name__ == '__main__':
    photo = Photo(sys.argv[1])
    photo.makeThumbnail('thumbs')
    photo.makePreview('previews')
