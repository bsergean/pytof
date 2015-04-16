#!/usr/bin/env python
"""pytof: Share your pictures.

pytof helps you share your iPhoto pictures, and any pictures that are stored in a flat directory since version 0.3.0. It works on Mac, Windows and Linux.
In this release
        ===============
        New in 0.8.2:
        - Put package on pypi.
        - Unit test works again
        - Do not chocke with movies
 
       New in 0.7.0:
       - Windows installer
       - Primitive user interface based on pygtk.
       - Image processing fallback to wxPython or pygtk if PIL is not installed
       - Play well with distutils, python setup.py install will put ctof.py (Command Line Interface) and gtof.py in your PATH
       - Several themes are available, and adding your own style should be easy (a wiki page to come soon).
       - Lots of PIL binaries (and python eggs) are available throught the download page
       - Create an index for all galleries, and there's an easy like in scry

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
	- You may have to call pytof from the source script directory, regular package install 
	  with python setup.py install was not tested. - if you can give it a try and report problems it is great
	  there might be problem finding the resources (.css files) then
	- Versionning is broken (issue 11)
	- Canceled operations should cleanup target dir (issue 13)
"""

classifiers = """\
Development Status :: 4 - Beta
Classifier: Environment :: Console (Text Based)
Intended Audience :: Developers
License :: OSI Approved :: GNU General Public License (GPL)
Programming Language :: Python
Topic :: Multimedia
Operating System :: Microsoft
Operating System :: MacOS
Operating System :: Unix
"""

# Copyright (C) 2006, 2007 GPL
# Written by Benjamin Sergeant <bsergean@gmail.com>

__revision__ = '$Id: ctof.py 308 2007-03-16 04:29:16Z bsergean $  (C) 2007 GPL'

from distutils.core import setup
import sys
from pytof.version import __version__

doclines = __doc__.split("\n")

def main():

    # data files
    # http://docs.python.org/dist/node13.html
    # http://www.thescripts.com/forum/thread164172.html
    # http://www.python.org/~jeremy/weblog/030924.html

    setup(
        name = "pytof",
        version = __version__,
        description = doclines[0],
        author = "Mathieu Robin",
        author_email = "mathieu.robin@gmail.com",
        maintainer = 'Benjamin Sergeant',
        maintainer_email = 'bsergean@gmail.com',
        url = 'http://code.google.com/p/pytof/',
        cmdclass = {},
        classifiers = filter(None, classifiers.split("\n")),
        long_description = "\n".join(doclines[2:]),
        scripts = ['ctof.py', 'gtof/gtof.py'],
        packages = ['pytof'],
#        package_dir = {'pytof': 'pytof'},
#        package_data = {'pytof': ['templates/*.css', 'templates/*.ezt']},
        data_files = [ ('share/pytof/templates', ['share/pytof/templates/scry_photo_per_page.ezt',
                                                  'share/pytof/templates/james_main_index.ezt',
                                                  'share/pytof/templates/james_gallery_index.ezt',
                                                  'share/pytof/templates/james_photo_per_page.ezt',
                                                  'share/pytof/templates/scry_main_index.ezt',
                                                  'share/pytof/templates/scry_gallery_index.ezt',
                                                  'share/pytof/templates/scry_photo_per_page.ezt']),
                       ('share/pytof/styles', ['share/pytof/styles/scry.css',
                                               'share/pytof/styles/james.css']),
                       ('share/pytof/glade', ['share/pytof/glade/gtof.glade'])]
        )

if __name__ == '__main__':
    main()
