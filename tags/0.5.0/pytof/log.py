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

loggers = {}
class Logger(object):

    def __init__(self):

        # FIXME: this may be a disaster when we will
        # use a package produced by a setup.py install
        self.pytofModules = []
        
        for i,j,files in walk(pardir):
            self.pytofModules.extend([py for py in files if py.endswith('.py')])
    
        for m in self.pytofModules:
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

    def quiet(self):
        ''' No fallback '''
        logging.disable(logging.ERROR)
        
# init ?
MainLogger = Logger()
