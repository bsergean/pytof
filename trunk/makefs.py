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
__dependencies__ = []

from os.path import expanduser, exists, join
from albumdataparser import AlbumDataParser
import os, sys, getopt
from utils import _err_, _err_exit, help, notYetImplemented

__version__ = '0.0.1'

def echo(s):
    sys.stdout.write(s)
    sys.stdout.flush()

def main(albumName, libraryPath, xmlFileName):
    """
    Just create a raw dir with all the picture from the album
    Will be used by scry after, for example.
    """
    notYetImplemented()
