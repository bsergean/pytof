#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- python -*-
#
#*****************************************************************************
#
# See LICENSE file for licensing and to see where does some code come from
#
#*****************************************************************************
#
# build package
#

from distutils.core import setup

def main():

    # data files
    # http://docs.python.org/dist/node13.html

    __version__ = open('VERSION').read()
    setup(
        name = "pytof",
        version = __version__,
        description = "Exports album from iPhoto Libraries",
        long_description = '''In this release
        ===============
    
        New in 0.0.2:
        
        - better navigation, makepage output looks almost like scry now
	- works on Linux with Panther iPhoto 2 and Tiger
	- cleaner help and option parsing thanks to optparse
	- xml file content is cached with cPickle and cache is used when the file hasn't changed
	- lots of bug fixes
	- regular python package (some problem, see first issue though, transition is not finished)

	Known issues:
	- You may have to pytof from the source script directory, regulare package install 
	  with python setup.py install wasn't tested. (if you can give it a try and report problems it's great
	  there might be problem finding the resources (.css files) then
	- Versionning is broken (issue 11)
	- Canceled operations should cleanup target dir (issue 13)
        
        ''',
        author = "Mathieu Robin",
        author_email = "mathieu.robin@gmail.com",
        maintainer = 'Benjamin Sergeant',
        maintainer_email = 'bsergean@gmail.com',
        url = 'http://code.google.com/p/pytof/',
        cmdclass = {},
        packages = ['pytof'],
        classifiers = [],
        scripts = ['scripts/pytof.py'],
        data_files = [ ('share', ['share/scry.css']) ]
        )

if __name__ == '__main__':
    main()
