#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- python -*-
#
#*****************************************************************************
#
# See LICENSE file for licensing and to see where does some code come from
#
#*****************************************************************************
#
# fs
#

__revision__ = '$Id: miscutils.py,v 1.17 2005/04/27 16:24:16 bsergean Exp $  (C) 2004 GPL'
__author__ = 'Benjamin Sergeant'

from albumdataparser import AlbumData
import os, sys

__version__ = '0.0.1'

def echo(s):
    sys.stdout.write(s)
    sys.stdout.flush()

def main(albumName, topDir, xmlData):
    """
    Just create a raw dir with all the picture from the album
    Will be used by scry after, for example.
    """

    photos = xmlData.getPicturesIdFromAlbumName(albumName)
    nb_photos = len(photos)
    cur = 1

    sys.stderr.write("Writing pictures\n")
    for pic_id in photos:
        photo = xmlData.getPhotoFromId(pic_id)
        photo.saveCopy(topDir)

        s = "\r%f %% - (%d processed out of %d) " \
            % (100 * float(cur) / float(nb_photos), cur, nb_photos)
        sys.stderr.write(s)
        cur += 1

    sys.stderr.write('\n')
