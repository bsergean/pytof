#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- python -*-
# $Id: makepage.py 42 2006-12-20 19:43:06Z bsergean $
#
#*****************************************************************************
#
# See LICENSE file for licensing and to see where does some code come from
#
#*****************************************************************************
#
# Main file.
#

__revision__ = '$Id: makepage.py 42 2006-12-20 19:43:06Z bsergean $  (C) 2004 GPL'
__author__ = 'Benjamin Sergeant'
__dependencies__ = []

from os.path import expanduser
from albumdataparser import AlbumDataParser
import os, sys, getopt
from utils import _err_, _err_exit, help

__version__ = '0.0.1'

if __name__ == "__main__":

    class BadUsage: pass
    try:
        libraryPath = ''
        fs = False

        # parse args
        if len(sys.argv) < 2:
            _err_('missing albumName argument')
            raise BadUsage
        albumName = sys.argv[-1]
        
        opts, args = getopt.getopt(sys.argv[1:], 'fVhl:')

        for opt, val in opts:
            if opt == '-h':
                raise BadUsage
            if opt == '-f':
                fs = True
            if opt == '-V':
                print 'pytof version %s' % (__version__)
                sys.exit(0)                             
            elif opt == '-l':
                libraryPath = val
                # ... how to get a parameter
            else:
                raise BadUsage

        if (fs):
            makefs.main(albumName, libraryPath)
        else:
            makepage.main(albumName, libraryPath)

    except (KeyboardInterrupt):
        _err_exit("Aborted by user")

    except (getopt.error, BadUsage):
        help(""" 
%s : Export iPhoto library

usage : python <program>.py <options> AlbumName
OPTIONS | -l <dir> : iPhoto library path
        | -v : display pytof version
        | -h : display this text
        | -f : extract album photo to a dir and stop
        """,
                       __revision__,
                       __dependencies__,
                       __author__)
