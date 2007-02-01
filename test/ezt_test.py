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

import os
from unittest import TestCase
from tempfile import mkdtemp, mktemp
from os.path import join, basename
from os import mkdir, listdir, getcwd
from shutil import copy, rmtree
from log import logger

from ezt import Template

class TestMakeFS(TestCase):

    def setUp(self):
        self.tempdir = mkdtemp()
        self.pytof = join('data', 'templates', 'pytof.ezt')
        self.perpage = join('data', 'templates', 'photo_per_page.ezt')
        self.pytofOutput = mktemp()
        print self.pytofOutput

    def tearDown(self):
        rmtree(self.tempdir)

    def _testTemplate(self, template, data, output = ''):
        if not output:
            output = self.pytofOutput
        pytofTemplate = Template(template)
        wfile = open(output, 'w')
        pytofTemplate.generate(wfile, data)

    def testMinimal(self):

        class Picture:
            def __init__(self, filename, href):
                self.filename = filename
                self.href = href

        pictures = [Picture('foo.jpg', 'foo.html'),
                    Picture('bar.jpg', 'bar.html')]
        title = 'template test'
        data = { 'title' : title, 'pictures' : pictures }
        data['gallery_name'] = 'Youpi Gallery'

        self._testTemplate(self.pytof, data)

    def testPerPhotoPage(self):
        '''
        One test would be to have a page already generated, regenerate it with the
        template and compare them.
        '''
        from photo import Photo
        photo = Photo(join('data', 'fake_iphoto_library', '2005',
                           '03', '23','rotated_minus_90.jpg'))
        prev = next = photo

        dico = {}
        dico['title'] = 'Youpi'
        dico['width'] = str(photo.width)
        dico['height'] = str(photo.height)
        dico['size'] = str(photo.sizeKB)
        dico['exif_infos'] = ('</br>').join(photo.exif_infos)
        dico['preview'] = join('preview', 'pv_' + photo.id + photo.getFileType())
        dico['preview_filename'] = basename(dico['preview'])
        dico['original'] = join('photos', photo.id + photo.getFileType())
        dico['prev'] = prev.id + '.html'
        dico['prev_thumb'] = join('thumbs',   'th_' + prev.id + prev.getFileType())
        dico['next'] = next.id + '.html'
        dico['next_thumb'] = join('thumbs',   'th_' + next.id + next.getFileType())

        self._testTemplate(self.perpage, dico)
