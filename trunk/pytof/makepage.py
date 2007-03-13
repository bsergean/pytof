#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- python -*-
# $Id$
#
#*****************************************************************************
#
# See LICENSE file for licensing and to see where does some code come from
#
#*****************************************************************************
#
# Main file.
#

__revision__ = '$Id$  (C) 2006 GPL'
__author__ = 'Mathieu Robin'

from log import logger
from os.path import join, exists, basename, isdir
from albumdataparser import AlbumDataFromDir
import os, sys
from utils import _err_exit, ProgressMsg
from template import pytofTemplate

def makePhotoPage(photo, topDir, prev, next, strip_originals, albumName, style):
    ''' 
    Create the per photo page, with a next and prev link
    Each link has a thumbnail in scry style mode
    '''
    dico = {}
    dico['album_name'] = albumName
    dico['title'] = photo.id + photo.getFileType()
    dico['width'] = str(photo.width)
    dico['height'] = str(photo.height)
    dico['size'] = str(photo.sizeKB)
    dico['exif_infos'] = photo.exif_infos
    dico['preview'] = '/'.join(['preview', 
				'pv_' + photo.id + photo.getFileType()])
    dico['preview_filename'] = basename(dico['preview'])
    dico['prev'] = prev.id + '.html'
    dico['prev_thumb'] = '/'.join(['thumbs', 
				   'th_' + prev.id + prev.getFileType()])
    dico['next'] = next.id + '.html'
    dico['next_thumb'] = '/'.join(['thumbs', 
				   'th_' + next.id + next.getFileType()])

    original = ('/').join(['photos', photo.id + photo.getFileType()])
    if strip_originals:
        original = ''
    dico['original'] = original

    pt = pytofTemplate()
    pt.write('photo', dico, join(topDir, photo.id) + '.html', style)

class Thumb:
    def __init__(self, page, image):
	self.page = page
	self.image = image

def main(albumName, topDir, xmlData, strip_originals,
         style, fromDir, progress=None):
    logger.info('strip_originals = %s' % strip_originals)
    if progress == None:
        progress = ProgressMsg(0, sys.stderr)
    data = xmlData
    if fromDir:
        data = AlbumDataFromDir(fromDir)

    leafDirs = ['photos', 'preview', 'thumbs']
    dirs = []
    for leafDir in leafDirs:
        Dir = join(topDir, leafDir)
        dirs.append(Dir)
        if not os.path.exists(Dir):
            try:
                os.makedirs(Dir)
            except (os.error):
                _err_exit('Cannot create %s' %(Dir))

    # Create magic file
    fo = open(join(topDir, '.magic'), 'w')
    fo.close()

    logger.info(topDir)

    # photo per page
    thumbs = []
    logger.info("Writing pictures\n")
    
    photos = data.getPicturesIdFromAlbumName(albumName)
    progress.target = len(photos)
    for i in xrange(len(photos)):

        pic_id = photos[i]
        logger.debug('processing photo %s' % pic_id)
        
        photo = data.getPhotoFromId(pic_id)
        prev = data.getPhotoFromId(photos[i-1])
        try:
            next = data.getPhotoFromId(photos[i+1])
        except (IndexError):
            # ok I know it's crappy programming :)
            next = data.getPhotoFromId(photos[0])

        if not strip_originals:
            photo.saveCopy(dirs[0])
        photo.makePreview(dirs[1], 640)
        photo.makeThumbnail(dirs[2])

        # FIXME: makePhotoPage return photoPageName which shoule be
        # modified to HTML/123.html. We would only have to create
        # a dir HTML, change the links in the index to HTML/123.html
        # and create the per page file in HTML/123.html
        makePhotoPage(photo, topDir,
                      prev, next,
                      strip_originals, albumName, style)
        thumbs.append(Thumb(photo.id + '.html',
                            '/'.join(['thumbs', 'th_' + photo.id + photo.getFileType()])))
        progress.Increment()


    # gallery index
    dico = {}
    dico['title'] = albumName
    dico['thumbs'] = thumbs

    pt = pytofTemplate()
    pt.write('index', dico, join(topDir, 'index') + '.html', style)

    # main index (list of all galleries)
    dico = {}
    dico['title'] = albumName
    dicoThumbs = []
    mainDir = join(topDir, os.pardir)
    logger.debug('main dir: %s' % mainDir)
    for album in os.listdir(mainDir):
	if not isdir(join(mainDir, album)): continue
	if not exists(join(mainDir, album, '.magic')): continue

	logger.debug('Found gallery %s' % album)
	thLink = '/'.join([album, 'index.html'])
	thDir = join(mainDir, album, 'thumbs')
	    
	thumbs = os.listdir(thDir)
	if len(thumbs) > 0:
	    thImage = '/'.join([albumName, 'thumbs', thumbs[0]])
	    dicoThumbs.append(Thumb(thLink, thImage))

    dico['gallery_thumb'] = dicoThumbs

    pt.write('main', dico, join(mainDir, 'index') + '.html', style)
