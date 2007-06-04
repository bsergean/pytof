#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- python -*-
#
#*****************************************************************************
#
# See LICENSE file for licensing and to see where does some code come from
#
#*****************************************************************************

__revision__ = '$Id$  (C) 2006 GPL'
__author__ = 'Benjamin Sergeant'

from os import remove, walk, chdir, getcwd
from os.path import join
from photo import EXIF_tags, Photo
from shutil import copy, rmtree
from tempfile import mkdtemp, mktemp
from utils import GetTmpDir
import os, sys
import unittest


def prune(tag, key):
    return str(tag[key])[0:-1]

def get_key(file, key, prune = False):
    tags = EXIF_tags(file)
    if key:
        if tags.has_key(key):
            if prune:
                return str(tags[key])[0:-1]
            else:
                return tags[key]


def print_tags(file):
    tags = EXIF_tags(file)
    for i in tags:
        if i not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename'):
            print '%s: %s' % (i, tags[i])

class TestEXIF(unittest.TestCase):
    '''
    This test needs some pictures in the data directory
    '''
    def setUp(self):
        self.tempdir = mkdtemp()
        self.exim1 = join('data',
                          'fake_iphoto_library',
                          '2005',
                          '03',
                          '23',
                          'rotated_minus_90.jpg')

    def tearDown(self):
        rmtree(self.tempdir)

    def test_exim1_print(self):
        verbose = False
        if verbose:
            print_tags(self.exim1)
              
    def test_exim1_assert_values(self):
        tags = EXIF_tags(self.exim1)
        self.assertEquals( str(tags['Image Model']), 'DSC-W1' )
        self.assertEquals( str(tags['Image Make']),'SONY' )
        self.assertEquals( str(tags['EXIF DateTimeOriginal']), '2005:01:29 16:59:27' )
        self.assertEquals( str(tags['EXIF Flash']), '77L' )

    def test_exim2_assert_values(self):
        photo = Photo(self.exim1)
        infos = photo.EXIF_infos()
        self.assertEquals('DSC-W1', infos.model)
        self.assertEquals('2005:01:29 16:59:27', infos.date)
        self.assertEquals('77L', infos.flash)
        
    def test_exif_assert_picture_is_rotated(self):
        key = 'Image Orientation'
        value = 'Rotated 90 CW'
        valueFromFile = str(get_key(self.exim1, key))
        self.assertEquals(value, valueFromFile)

    def _auto_rotate_thanks_to_exif(self, thumb = True):

        tgetDir = 'thumbs'
        if not thumb:
            tgetDir = 'preview'
        
        tmpFile = join(self.tempdir, 'toto.jpg')
        copy(self.exim1, tmpFile)

        oldpwd = getcwd()
        chdir(self.tempdir)
        
        photo = Photo(tmpFile)
        tmpDir = join(self.tempdir, tgetDir)
        os.mkdir(tmpDir)

        if not thumb:
            photo.makeThumbnail(tgetDir)
        else:
            photo.makePreview(tgetDir)

        #for d in walk(self.tempdir):
        #    print d

        # uncomment to get this picture and check it (I use the handy xv)
        #copy(photo.thumbPath, '/tmp/thumb.jpg')

        chdir(oldpwd)

    def test_auto_rotate_thumbnail_thanks_to_exif(self):
        self._auto_rotate_thanks_to_exif(thumb = True)
    
    def test_auto_rotate_preview_thanks_to_exif(self):
        self._auto_rotate_thanks_to_exif(thumb = False)

    def test_undefined_tags(self):
        exim1 = join('data', 'NoExifTags.jpg') 
        tags = EXIF_tags(exim1)
        self.assertEquals(tags,{})       

if __name__ == "__main__":
    unittest.main()
