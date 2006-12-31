#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- python -*-
#
#*****************************************************************************
#
# See LICENSE file for licensing and to see where the code comes from
#
#*****************************************************************************

__revision__ = '$Id$  (C) 2004 GPL'
__author__ = 'Benjamin Sergeant'

import logging

pytofModules = ['pytof.py',
                'albumdataparser.py',
                'configFile.py',
                'ftp.py',
                'makepage.py',
                'utils.py',
                'EXIF.py',
                'makefs.py',
                'photo.py']

loggers = {}
for m in pytofModules:
    module = m.split('.')[0]

    logger = logging.getLogger(module)
    logger.setLevel(logging.DEBUG)

    #create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    #create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    #add formatter to ch
    ch.setFormatter(formatter)

    #add ch to logger
    logger.addHandler(ch)

    loggers[module] = logger
