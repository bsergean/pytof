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

import sys
import logging
from unittest import TestCase
from log import logger

class MockStream(object):
    def __init__(self):
        self.data = ""
    def write(self, line):
        self.data += line
    def flush(self):
        pass
        
class TestLog(TestCase):
    def test_simple_log(self):
        #create logger
        logger = logging.getLogger("simple_example")
        logger.setLevel(logging.DEBUG)
        stream = MockStream()
        
        #create handler and set level to debug
        handler = logging.StreamHandler(stream)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

        #add ch to logger
        logger.addHandler(handler)
    
        #"application" code
        logger.debug("debug message")
        logger.info("info message")
        logger.warn("warn message")
        logger.error("error message")
        logger.critical("critical message")
        
        expectedMsgEnds = [" - simple_example - DEBUG - debug message",
                           " - simple_example - INFO - info message",
                           " - simple_example - WARNING - warn message",
                           " - simple_example - ERROR - error message",
                           " - simple_example - CRITICAL - critical message", ""]
               
        for i, line in enumerate(stream.data.split("\n")):
            self.assert_(line.endswith(expectedMsgEnds[i]))
