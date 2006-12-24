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

    setup(
        name = "pytof",
        version = '0.0.2',
        description = "Exports album from iPhoto Libraries",
        long_description = '''In this release
        ===============
    
        Fixed in 0.0.2:
        
        A lot :)
        
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
