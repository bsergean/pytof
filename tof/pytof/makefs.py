"""
Create a directory with all the originals from a gallery.
Mainly used in conjunction with iPhoto, where pictures are kindof stucked.
Usefull to backup your pictures, or to give to a webbased (php ?) system
like scry.
"""

# Copyright (C) 2006, 2007 GPL
# Rewritten by Benjamin Sergeant <bsergean@gmail.com>

__revision__ = '$Id$  (C) 2007 GPL'

from utils import ProgressMsg
import sys

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
        if photo.ok:
		    photo.saveCopy(topDir)
        progress.Increment()
