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

import sys
import os
import time
import unittest
from glob import glob
import coverage, colorize

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
    

def runTests(testModules=None, profileOut=None, coverageOutDir=None):
    if coverageOutDir is not None:
        if not os.path.exists(coverageOutDir):
            os.makedirs(coverageOutDir)
        coverage.erase()
        coverage.start()
        
    alltests = unittest.TestLoader().loadTestsFromNames(testModules)
    
    if profileOut is not None:
        results = Profiler().profile(alltests)
        results.sort()
        results.reverse()
        for result in results:
            profileOut.write("%s  \t%3.6f\n" % (result[1], result[0]))
            print "Profiling information written in " + profileOut.name
        profileOut.close()
    
    unittest.TextTestRunner().run(alltests)

    if coverageOutDir is not None:
        coverage.stop()
        modules = glob('../pytof/*.py')
        modules.remove('../pytof/__init__.py')
                
        for module in modules:
            f, s, m, mf = coverage.analysis(module)
            out = file(os.path.join(coverageOutDir, os.path.basename(f)+'.html'), 'wb')
            colorize.colorize_file(f, outstream=out, not_covered=mf)
            out.close()
        print
        coverageReportTxt = file(os.path.join(coverageOutDir, "coverage.txt"), 'w')
        coverage.report(modules, show_missing=False, omit_prefixes=['__'], file=coverageReportTxt) 
        coverageReportTxt.close()
        coverage.report(modules, show_missing=False, omit_prefixes=['__'])
        coverage.erase()
        
        coverageReportTxt.close()
        print
        print "Coverage information updated in " + coverageOutDir
        print
        

if __name__ == '__main__':
    import getopt
    try:
        options, args = getopt.getopt(sys.argv[1:], 't:pc', [])
    except getopt.GetoptError, (msg, opt):
        print "ERROR: " + msg
        sys.exit(2)
    
    testModules = tuple( [os.path.splitext(i)[0] for i in glob('*_test.py')] )

    profileOut = None
    coverageOutDir = None
    for option, arg in options:
        if option == "-t":
            names = arg.split(',')
            testModules = ()
            for name in names:
                testModules += (name,)
        elif option == "-p":
            if arg == "":
                arg = "output/profile.txt"
            profileOut = file(arg, 'w')
        elif option == "-c":
            if arg == "":
                arg = "output/coverage/"
            coverageOutDir = arg

    runTests(testModules, profileOut, coverageOutDir)
    
