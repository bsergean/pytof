#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- python -*-
#
#*****************************************************************************
#
# See LICENSE file for licensing and to see where does some code come from
#
#*****************************************************************************

__revision__ = '$Id: ftp_test.py 149 2007-01-08 22:31:28Z mathieu.robin $  (C) 2007 GPL'


from unittest import TestCase
import utils


class TestUtils(TestCase):
    def testRemoveSpecificChars(self):
        testCases = [
            ["test1", "test1"],
            ["test2(", "test2"]]
        for case in testCases:
            self.assertEquals(case[1], utils.RemoveSpecificChars(case[0]))
