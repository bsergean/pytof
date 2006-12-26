#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- python -*-
#
#*****************************************************************************
#
# See LICENSE file for licensing and to see where does some code come from
#
#*****************************************************************************

__revision__ = '$Id: utils.py 67 2006-12-22 22:53:55Z bsergean $  (C) 2004 GPL'
__author__ = 'Benjamin Sergeant'

import sys
sys.path.insert(1, '../pytof')

import os
from os import remove
from utils import GetTmpDir
from photo import EXIF_infos, EXIF_tags

def prune(tag, key):
    return str(tag[key])[0:-1]

if __name__ == "__main__":

    exim1 = os.path.join('data', 'exim1.jpg')
    # FIXME: add other picture taken from different camera

    tags = EXIF_tags(exim1)
    k=tags.keys()

    # print all tags
    verbose = False
    if verbose:
        for i in k:
            if i not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename'):
                print '%s: %s' % (i, tags[i])

    assert prune(tags, 'Image Model') == 'PENTAX Optio S5i'
    assert prune(tags, 'Image Make') == 'PENTAX Corporation'

    assert str(tags['EXIF DateTimeOriginal']) == '2005:04:10 17:52:16'
    assert str(tags['EXIF Flash']) == 'Off'

    print ('\n').join(EXIF_infos(exim1))
