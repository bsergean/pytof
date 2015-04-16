#!/usr/bin/env python
"""
CLI (command line interface) main driver for pytof.
"""

# Copyright (C) 2006, 2007 GPL
# Written by Benjamin Sergeant <bsergean@gmail.com>

__revision__ = '$Id$  (C) 2007 GPL'

import os, sys
from pytof.options import PytofOptions
from pytof.pytofmain import Pytof
from pytof.utils import ProgressMsg

if __name__ == "__main__":
    # Import Psyco (will speedup program) if available
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass

    po = PytofOptions()
    po.check()

    # FIXME: there's gonna be a problem if we have a a comma
    # in the album name.
    for album in po.options.albumName.split(','):

	po.options.albumName = album

        progress = ProgressMsg(-1, sys.stderr)
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

