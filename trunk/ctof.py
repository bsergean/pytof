#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- python -*-
#*****************************************************************************
#
# See LICENSE file for licensing and to see where does some code come from
#
#*****************************************************************************
#
# Main file.
#

__revision__ = '$Id$  (C) 2006 GPL'
__author__ = 'Benjamin Sergeant'

import os, sys
from pytof.options import pytofOptions
from pytof.pytofmain import Pytof
from pytof.utils import ProgressMsg

if __name__ == "__main__":
    # Import Psyco (will speedup program) if available
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass

    po = pytofOptions()
    po.check()
    progress = ProgressMsg(-1, sys.stderr)

    # FIXME: there's gonna be a problem if we have a a comma
    # in the album name.
    for album in po.options.albumName.split(','):

	po.options.albumName = album

	pytof = Pytof(po, progress)
	if po.options.pyprofile:

	    # FIXME: factorize me in utils
	    from profile import Profile
	    myprofiler = Profile()
	    myprofiler.create_stats()

	    myprofiler.runcall(pytof.main)

	    from tempfile import mktemp
	    statfile = mktemp()
	    myprofiler.dump_stats(statfile)

	    import pstats
	    p = pstats.Stats(statfile)
	    os.remove(statfile) # remove temp file
	    p.strip_dirs()
	    p.sort_stats('cumulative').print_stats(30)

	else:

	    pytof.main()

