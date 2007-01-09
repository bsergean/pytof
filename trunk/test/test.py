#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- python -*-
#
#*****************************************************************************
#
# See LICENSE file for licensing and to see where does some code come from
#
#*****************************************************************************

__revision__ = '$Id$  (C) 2007 GPL'
__author__ = 'Mathieu Robin'

import sys, time
import unittest

if 'check' in sys.argv[1:]:
    __pychecker__ = 'no-deprecated no-miximport'
    import pychecker.checker

sys.path.insert(1, '../pytof')

class Profiler(object):
    def profile(self, alltests):
        results = []
        self.profileTests(alltests._tests, results)
        return results
    
    def profileTests(self, tests, results):
        totalTime = 0
        for test in tests:
            if hasattr(test, '_tests'):
                totalTime += self.profileTests(test._tests, results)
            else:
                startTime = time.time()
                test.debug()
                stopTime = time.time()
                testTime = stopTime - startTime
                results.append((testTime, test.id()))
                totalTime += testTime
        return totalTime
    

def runTests(testModules=None, profileOut=None):
    alltests = unittest.TestLoader().loadTestsFromNames(testModules)
    
    if profileOut is not None:
        results = Profiler().profile(alltests)
        results.sort()
        results.reverse()
        for result in results:
            profileOut.write("%s  \t%3.6f\n" % (result[1], result[0]))
        profileOut.close()
    
    unittest.TextTestRunner().run(alltests)


if __name__ == '__main__':
    import getopt
    try:
        options, args = getopt.getopt(sys.argv[1:], 't:p:', [])
    except getopt.GetoptError, (msg, opt):
        print "ERROR: " + msg
        sys.exit(2)
    
    testModules = ('config_test', 'exif_test', 'ftp_test',
                   'log_test', 'makepage_test', 'utils_test')

    profileOut = None
    for option, arg in options:
        if option == "-t":
            names = arg.split(',')
            testModules = ()
            for name in names:
                testModules += (name,)
        elif option == "-p":
            if arg == "":
                arg = "profile.txt"
            profileOut = file(arg, 'w')
    runTests(testModules, profileOut)
    
