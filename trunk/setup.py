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

    roundup_scripts = 'scripts/pytof.py'
    installdatafiles = [
        'share/style.css',
    ]
    
    setup_args = {
        'name': "pytof",
        'version': '0.0.2',
        'description': "Exports album from iPhoto Libraries",
        'long_description':
'''In this release
===============

Fixed in 0.0.2:

''',
        'author': "Benjamin Sergeant",
        'author_email': "bsergean@gmail.com",
        'url': 'http://code.google.com/p/pytof/',

        'scripts': roundup_scripts,
        'data_files':  installdatafiles

    }
    setup(**setup_args)

if __name__ == '__main__':
    main()
