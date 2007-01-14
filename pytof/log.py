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

from os import listdir, chdir, pardir, getcwd, walk
from os.path import join
from glob import glob

format = "%(asctime)s - %(module)s - %(levelname)s - %(message)s"

#create logger
logger = logging.getLogger('pytof')
logger.setLevel(logging.DEBUG)

#create handler and set level to debug
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter(format))

#add ch to logger
logger.addHandler(handler)

def quiet():
    logger.setLevel(logging.WARNING)
