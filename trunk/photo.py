#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- python -*-
# $Id: pyfind.py 29 2006-12-12 20:47:34Z bsergean $
#
#*****************************************************************************
#
# See LICENSE file for licensing and to see where does some code come from
#
#*****************************************************************************

import Image
import sys, os, time


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

    def getBaseName(self):
        return str(self.id)

    def getFileType(self):
        return os.path.basename(self.fileName).split('.')[-1].lower()

    def saveCopy(self, path):
        self.imagePath = os.path.join(path, self.getBaseName() + '.' +
                                        self.getFileType())
        input = file(self.fileName, 'r')
        output = file(self.imagePath, 'w')
        output.write(input.read())

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
