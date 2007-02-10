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
from os import getcwd
from os.path import join
from unittest import TestCase

if 'check' in sys.argv[1:]:
    __pychecker__ = 'no-deprecated no-miximport'
    import pychecker.checker

sys.path.insert(1, '../pytof')

from utils import mkarchive, maybemakedirs, lpathstrip, create
from os.path import join, getsize
from tempfile import mkdtemp, mktemp
from shutil import rmtree, copytree
from os import mkdir
from optparse import OptionParser


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
    
class PytofTestCase(TestCase):

    def setUp(self):
        self.tempdir = mkdtemp()
        self.galleries = join('data', 'galleries')

    def tearDown(self):
        try:
            rmtree(self.tempdir)
        except OSError: pass

    def create_dummy_dir(self, newDir):
        '''
        This one is duplicated from ftp_utils: We should create a class
        that inherit unittest.TestCase, with this method in it in test.py.
        We should take care of the self.tmpdir also.
        '''
        topDir = join(self.tempdir, newDir)
        maybemakedirs(topDir)

        # first level
        tmpftpfile = 'level_1_fileA'
        create(join(self.tempdir, tmpftpfile), 'youcoulele')
        tmpftpfile = 'level_1_fileB'
        create(join(self.tempdir, tmpftpfile), 'warzazat')

        # second level
        tmpftpfile = 'level_2_fileA'
        create(join(topDir, tmpftpfile), 'youcoulele')

        # third level A
        nestedDir = join(topDir, 'a_dir')
        mkdir(nestedDir)

        tmpftpfile = 'level_3A_fileA'
        create(join(nestedDir, tmpftpfile), 'youcoulele')
        tmpftpfile = 'level_3A_fileB'
        create(join(nestedDir, tmpftpfile), 'warzazat')

        # third level B
        nestedDir = join(topDir, 'b_dir')
        mkdir(nestedDir)

        tmpftpfile = 'level_3A_fileA'
        create(join(nestedDir, tmpftpfile), 'makelele')
        tmpftpfile = 'level_3B_fileB'
        create(join(nestedDir, tmpftpfile), 'bogoss')

        return topDir

    

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
            out = file(join(coverageOutDir, os.path.basename(f)+'.html'), 'wb')
            colorize.colorize_file(f, outstream=out, not_covered=mf)
            out.close()
        print
        coverageReportTxt = file(join(coverageOutDir, "coverage.txt"), 'w')
        coverage.report(modules, show_missing=False, omit_prefixes=['__'], file=coverageReportTxt) 
        coverageReportTxt.close()
        coverage.report(modules, show_missing=False, omit_prefixes=['__'])
        coverage.erase()
        
        coverageReportTxt.close()
        print
        print "Coverage information updated in " + coverageOutDir
        print

        import webbrowser
        webbrowser.open('file://' + join(getcwd(), coverageOutDir))


class ArgsOptions(object):

    def __init__(self):
        # parse args
        usage = "usage: python %prog <options>"
        parser = OptionParser(usage=usage)

        parser.add_option("-c", "--coverage", action="store_true", dest="coverage",
                          help="Enable coverage testing")
        parser.add_option("-p", "--profile", action="store_true", dest="profile",
                          help="Enable profiling")
        
        parser.add_option("-C", "--coverage-filename", dest="coverageOutDir",
                          help="The coverage test output directory [%default]")
        parser.add_option("-P", "--profile-filename", dest="profileOut",
                          help="The output profile filename [%default]")
        parser.add_option("-l", "--list", dest="testModules",
                          help="The list of module to test [%default]")

        defaultTestModules = tuple( [os.path.splitext(i)[0] for i in glob('*_test.py')] )

        parser.set_defaults(
            testModules = defaultTestModules,
            profile = False,
            profileOut = join('output','profile.txt'),
            coverage = False,
            coverageOutDir = join('output','coverage'))
        
        self.options, args = parser.parse_args()

        if self.options.testModules != defaultTestModules:
            self.options.testModules = tuple(self.options.testModules.split(','))

        if not self.options.coverage:
            self.options.coverageOutDir = None
        if not self.options.profile:
            self.options.profileOut = None

if __name__ == '__main__':

    try:
        ao = ArgsOptions()
        runTests(ao.options.testModules,
                 ao.options.profileOut,
                 ao.options.coverageOutDir)

        # On windows, we make a dummy raw_input so that the 
        # python terminal does not shut down after exiting
        if os.name == 'nt': 
            raw_input()
            
    except(KeyboardInterrupt):pass
    
