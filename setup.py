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
import sys
from pytof.version import __version__

pytof_long_description = '''
In this release
        ===============

	New in 0.2.0:

        Now you can generate *light* galleries, which means that you can strip the originals pictures. Those galleries are smaller and can easily be sent by email (with some limits of course :).

        - Enhancements: (Issues 16, 20)

	New in 0.0.1:
	- Enhancements: (Issues 15, 17, 19, 21)
	- Defects: (Issues 11, 13)

        New in 0.0.2:
        
        - better navigation, makepage output looks almost like scry now
	- works on Linux with Panther iPhoto 2 and Tiger
	- cleaner help and option parsing thanks to optparse
	- xml file content is cached with cPickle and cache is used when the file has not changed
	- lots of bug fixes
	- regular python package (some problem, see first issue though, transition is not finished)
	Known issues:
	- You may have to pytof from the source script directory, regular package install 
	  with python setup.py install was not tested. - if you can give it a try and report problems it is great
	  there might be problem finding the resources (.css files) then
	- Versionning is broken (issue 11)
	- Canceled operations should cleanup target dir (issue 13)
'''

def main():

    # data files
    # http://docs.python.org/dist/node13.html
    # http://www.thescripts.com/forum/thread164172.html

    setup(
        name = "pytof",
        version = __version__,
        description = "Exports album from iPhoto Libraries",
        long_description = pytof_long_description,
        author = "Mathieu Robin",
        author_email = "mathieu.robin@gmail.com",
        maintainer = 'Benjamin Sergeant',
        maintainer_email = 'bsergean@gmail.com',
        url = 'http://code.google.com/p/pytof/',
        cmdclass = {},
        classifiers = [],
        scripts = ['scripts/pytof.py'],

        packages = ['pytof'],
        package_dir = {'pytof': 'pytof'},
        package_data = {'pytof': ['templates/*.css', 'templates/*.ezt']},
#	data_files = [ ('templates', ['templates/scry_photo_per_page.ezt',
#                                      'templates/james_main_index.ezt',
#                                      'templates/james_gallery_index.ezt',
#                                      'templates/james_photo_per_page.ezt',
#                                      'templates/scry_main_index.ezt',
#                                      'templates/scry_gallery_index.ezt',
#                                      'templates/scry_photo_per_page.ezt']),
#                        ('share',    ['share/scry.css',
#                                      'share/james.css'])]
        )

if __name__ == '__main__':
    main()
