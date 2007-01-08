#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- python -*-
#
#*****************************************************************************
#
# See LICENSE file for licensing and to see where does some code come from
#
#*****************************************************************************

__revision__ = '$Id$  (C) 2004 GPL'
__author__ = 'Benjamin Sergeant'

from config import configHandler
from os import remove
from unittest import TestCase


class TestConfigHandler(TestCase):
    def testInit(self):
        conf = configHandler('data/conf')
        self.assertEquals("data/conf/pytof.ini", conf.confFilename)
    
    # TODO: Write a more complex pytof.ini file to test everything