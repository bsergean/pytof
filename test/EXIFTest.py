#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- python -*-
#
#*****************************************************************************
#
# See LICENSE file for licensing and to see where does some code come from
#
#*****************************************************************************

__revision__ = '$Id$  (C) 2004 GPL'
__author__ = 'Benjamin Sergeant'

import sys
sys.path.insert(1, '../pytof')

import os
from os import remove
from utils import GetTmpDir
from photo import EXIF_infos, EXIF_tags

def prune(tag, key):
    return str(tag[key])[0:-1]

def print_tags(file):
    tags = EXIF_tags(file)
    for i in tags:
        if i not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename'):
            print '%s: %s' % (i, tags[i])


if __name__ == "__main__":

    exim1 = os.path.join('data', 'exim1.jpg')
    # FIXME: add other picture taken from different camera

    tags = EXIF_tags(exim1)
    k=tags.keys()

    # print all tags
    verbose = False
    if verbose:
        print_tags(exim1)
        
    assert prune(tags, 'Image Model') == 'PENTAX Optio S5i'
    assert prune(tags, 'Image Make') == 'PENTAX Corporation'

    assert str(tags['EXIF DateTimeOriginal']) == '2005:04:10 17:52:16'
    assert str(tags['EXIF Flash']) == 'Off'

    print ('\n').join(EXIF_infos(exim1))

    exim2 = os.path.join('data', 'Rotated_90_CW_thumb.jpg')
    

    print_tags(exim2)
    # looks like PIL remove
    keys = {}
    keys['Image Orientation'] = 'Rotated 90 CW'
