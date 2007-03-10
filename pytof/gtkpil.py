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
__author__ = 'Benjamin Sergeant'

import gtk

# dummy global for compat
ANTIALIAS = True

def open(fn):
    return Image(fn)

class Image:
    '''
    http://www.pygtk.org/docs/pygtk/class-gdkpixbuf.html
    '''
    def __init__(self, fn):
        self.image = gtk.gdk.pixbuf_new_from_file(fn)
        self.setSize()

    def fromImage(self, image, size):
        self.image = image
        self.size = size
        return self

    def setSize(self):
        self.size = [self.image.get_width(),
                     self.image.get_height()]
        return self.size

    def crop(self, rect):
        x1, y1, x2, y2 = rect
        self.image = self.image.subpixbuf(x1, y1, x2 - x1, y2 - y1)
        return self.fromImage(self.image, self.setSize())

    def resize(self, size, dummy):
        '''
        size = x, y (a 2-uple ?)
        '''
        x, y = size
        self.image = self.image.scale_simple(x, y, gtk.gdk.INTERP_BILINEAR)
        return self.fromImage(self.image, self.setSize())
    
    def rotate(self, angle):
        self.image = self.image.rotate_simple(90) # default Rotate90 is clockwise=True
        return self.fromImage(self.image, self.setSize())

    def save(self, path, quality):
        options = {}
        # FIXME: there may be faster to check if it's a valid digit
        # but do we care here ... :)
        if not str(quality).isdigit() or quality < 0 or quality > 100:
            quality = 100
        options['quality'] = str(quality)
        self.image.save(path, "jpeg", options)
