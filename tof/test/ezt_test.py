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
        self.index = join('data', 'templates', 'gallery_index.ezt')
        self.pytofOutput = mktemp()
        #print self.pytofOutput

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

    def _testPerPhotoPage(self, strip_originals):
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

	class _datablob:
	    def __init__(self, **args):
		self.__dict__.update(args)

        infos = _datablob()
        infos.model = 'le super appareil de la mort'
        infos.date = 'premier janvier 2012'
        infos.flash = 'flash avec les yeux rouges'
        
        dico['exif_infos'] = infos
        dico['preview'] = join('preview', 'pv_' + photo.id + photo.getFileType())
        dico['preview_filename'] = basename(dico['preview'])
        dico['prev'] = prev.id + '.html'
        dico['prev_thumb'] = join('thumbs',   'th_' + prev.id + prev.getFileType())
        dico['next'] = next.id + '.html'
        dico['next_thumb'] = join('thumbs',   'th_' + next.id + next.getFileType())

        original = join('photos', photo.id + photo.getFileType())
        if strip_originals:
            original = ''
        dico['original'] = original

        self._testTemplate(self.perpage, dico)

    def testPerPhotoPageOriginals(self):
        self._testPerPhotoPage(strip_originals = True)

    def testPerPhotoPageNoOriginals(self):
        self._testPerPhotoPage(strip_originals = False)

    def testGalleryIndex(self):
        class Thumb:
            def __init__(self, page, image):
                self.page = page
                self.image = image

        thumbs = []
        thumbs.append(Thumb('foo.html', 'foo.jpg'))
        thumbs.append(Thumb('bar.html', 'bar.jpg'))
        thumbs.append(Thumb('buz.html', 'buz.jpg'))

        dico = {}
        dico['title'] = 'Youpi'
        dico['thumbs'] = thumbs

        self._testTemplate(self.index, dico)
