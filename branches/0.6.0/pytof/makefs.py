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

__revision__ = '$Id$  (C) 2004 GPL'
__author__ = 'Benjamin Sergeant'

from albumdataparser import AlbumData
from utils import ProgressMsg
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

    sys.stderr.write("Writing pictures\n")
    progress = ProgressMsg(len(photos), output=sys.stderr)
    for pic_id in photos:
        photo = xmlData.getPhotoFromId(pic_id)
        photo.saveCopy(topDir)
        progress.Increment()
