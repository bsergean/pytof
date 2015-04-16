"""
Interface to PIL Image class implemented with wxPython code
"""

# Copyright (C) 2006, 2007 GPL
# Written by Benjamin Sergeant <bsergean@gmail.com>

__revision__ = '$Id$  (C) 2007 GPL'

import wx

# dummy global for compat
ANTIALIAS = True

def open(fn):
    return Image(fn)

class Image:
    '''
    TODO: Try to load only Image, Point and Size to avoid poluting namespace
    Thumb quality is bad, cropping does not work ... still some work to do

    It looks like there is no antialiasing.
    '''
    def __init__(self, fn):
        self.image = wx.Image(fn)
        self.setSize()

    def fromImage(self, image, size):
        self.image = image
        self.size = size
        return self

    def setSize(self):
        self.size = [self.image.GetWidth(),
                     self.image.GetHeight()]
        return self.size

    def crop(self, rect):
        x1, y1, x2, y2 = rect
        self.image = self.image.GetSubImage(wx.Rect(x1, y1, x2 - x1, y2 - y1))
        return self.fromImage(self.image, self.setSize())

    def resize(self, size, dummy):
        '''
        size = x, y (a 2-uple ?)
        '''
        x, y = size
        self.image = self.image.Scale(x, y)
        return self.fromImage(self.image, self.setSize())
    
    def rotate(self, angle):
        self.image = self.image.Rotate90() # default Rotate90 is clockwise=True
        return self.fromImage(self.image, self.setSize())

    def save(self, path, quality):
        self.image.SaveFile(path, wx.BITMAP_TYPE_JPEG)
