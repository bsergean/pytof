"""
Interface for storing albums informations.
Albums can be flat directory full of images, or iPhoto galleries.
iPhoto galleries are stored in xml (plist) files.
"""

# Copyright (C) 2006, 2007 GPL
# Written by Benjamin Sergeant <bsergean@gmail.com>

__revision__ = '$Id$  (C) 2007 GPL'

from log import logger

import os
from os.path import expanduser, exists, join, split, splitext, basename
from xml.parsers.expat import ParserCreate, ExpatError
from photo import Photo
from utils import _err_, _err_exit, ListCurrentDirFileFromExt
from time import strptime
from cPickle import dump, load

class AlbumDataFromDir(object):
    def __init__(self, path):

        self.path = path
        self.albumList = ListCurrentDirFileFromExt('jpg', self.path)
        logger.debug('pictures: %s' % self.albumList)
        
        self.picturesIds = {}
        for p in self.albumList:
            pic_id = splitext(split(p)[1])[0]
            self.picturesIds[pic_id] = p
        logger.debug('pictures id: %s' % self.picturesIds)

    def getPicturesIdFromAlbumName(self, name):
        keys = self.picturesIds.keys()
        keys.sort()
        logger.info('keys: %s' % keys)
        return keys

    def getAlbumByName(self, name):
        return basename(split(self.path)[0])

    def getPhotoFromId(self, pic_id):
        # FIXME: this None list is so nice.
        return Photo(self.picturesIds[pic_id],
                     pic_id,
                     None,
                     None,
                     None)

class AlbumDataError(Exception): pass
class AlbumData(object):
    def __init__(self, data, libraryPath):
        self.data = data
        self.libraryPath = libraryPath

    def getAlbumByName(self, name):
        for album in self.data['List of Albums']:
            if album['AlbumName'] == name:
                return album
        raise AlbumDataError, "Album \"%s\" not in iPhoto Library" % name

    def getAlbumList(self):
        albums = []
        for album in self.data['List of Albums']:
            a = album['AlbumName']
            # FIXME: maybe there's a better way of filtering
            # (another meta data saying it's a book ...)
            if not a.endswith('Book') and not a.startswith('Livre') and not a.startswith('Diaporama'):
                albums.append( [int(album['PhotoCount']), a] )

        # to sort by date, we would have to compute the date mean of
        # an album ... so we sort by the bigger album for now
        albums.sort()
        return [album[1] for album in albums]

    def getPicturePathFromId(self, pic_id):
        return self.data['Master Image List'][pic_id]['ImagePath']

    def getPicturesIdFromAlbumName(self, name):
        ''' 
        Skip movies, only return a list of pictures 
        The ok member tells if a photo is really a photo, and not 
        just a file given by iPhoto
        '''
        album = self.getAlbumByName(name)
        album = album['KeyList']
        pictureAlbum = [picture for picture in album if self.getPhotoFromId(picture).ok]
        return pictureAlbum

    def getPhotoFromId(self, pic_id):
        p = self.data['Master Image List'][pic_id]
        photoFileName = p['ImagePath']

	# FIXME: This is a mess:
	# Can we simplify it with dictionnaries and / or regexp ?
        if self.libraryPath:
            try:
                if 'Originals' in photoFileName:
                    index = photoFileName.index('Originals')
                    photoFileName = join(self.libraryPath, photoFileName[index:])
                elif 'Modified' in photoFileName:
                    index = photoFileName.index('Modified')
                    photoFileName = join(self.libraryPath, photoFileName[index:])
                else:
                    # iPhoto 2 (Panther)
		    if 'iPhoto Library' in photoFileName:
			suffix = photoFileName.split('iPhoto Library' + '/')[1]
		    elif 'iPhotoLibrary' in photoFileName:
			suffix = photoFileName.split('iPhotoLibrary' + '/')[1]
                    photoFileName = join(self.libraryPath, suffix)
                    
            except (ValueError):
                # probably panther iPhoto, there is no Original in the filename
                print self.libraryPath
                _err_exit('Internal Error: cannot handle %s' %(photoFileName))

            logger.info(photoFileName)
        else:
            raise AlbumDataError, "Internal error: libraryPath not defined"

        if not p.has_key('DateAsTimerInterval'):
            p['DateAsTimerInterval'] = ''
            
        return Photo(photoFileName,
                     pic_id,
                     p['Caption'],
                     p['Comment'],
                     p['DateAsTimerInterval'])

    def getPhotosFromAlbumName(self, name):
        res = []
        pics = self.getPicturesIdFromAlbumName(name)
        for pic in pics:
            res.append(self.getPhotoFromId(pic))
        return res

    def info(self, name):
        photos = self.getPicturesIdFromAlbumName(name)
        for pic_id in photos:
            print pic_id

class XmlItem(object):
    def __init__(self, type):
        self.type = type
        self.value = None

    def setValue(self, val):
        if self.type == 'key':
            self.value = val
        elif self.type == 'string':
            self.value = val.encode('utf8')
        elif self.type == 'integer':
            self.value = int(val)
        elif self.type == 'real':
            self.value = float(val)
        elif self.type == 'true':
            self.value = True
        elif self.type == 'false':
            self.value = False
        elif self.type == 'date':
            # if I put this import in the global scopre I have an error ... ???:
            # self.value = datetime(*strptime(val, '%Y-%m-%dT%H:%M:%SZ')[:5])
            # UnboundLocalError: local variable 'datetime' referenced before assignment
            from datetime import datetime
            self.value = datetime(*strptime(val, '%Y-%m-%dT%H:%M:%SZ')[:5])
        else:
            raise ExpatError, "Type \"%s\" not supported" % type

class AlbumDataParserError(Exception): pass
class AlbumDataParser(object):
    def __init__(self,
                 xmlFileDir,
                 xmlFileBaseName):
        if not xmlFileDir:
            xmlFileDir = expanduser('~/Pictures/iPhoto Library')
        if not xmlFileBaseName:
            xmlFileBaseName = 'AlbumData.xml'

        self.xmlFileDir = xmlFileDir
        xmlFileName = join(self.xmlFileDir, xmlFileBaseName)
        if not exists(xmlFileName):
            _err_('\nNo xml file found at %s' %(xmlFileName))
            raise AlbumDataParserError

        self.xmlFileName = xmlFileName
        self.xmlFile = file(xmlFileName, 'r')
        self.elemList = []
        self.lastItemData = ''
        self.keys = []
        self.albumData = None        
        self.parsed = False

    def addItem(self, item):
            liste = self.elemList[-1]
            if str(liste.__class__) == "<type 'dict'>":
                liste[self.keys.pop()] = item
            elif str(liste.__class__) == "<type 'list'>":
                liste.append(item)
            else:
                raise ExpatError, list.__class__

    def parse(self):
        from PListReader import PListReader
        reader = PListReader()
        import xml.sax
        parser = xml.sax.make_parser()
        parser.setContentHandler(reader)
        parser.setFeature(xml.sax.handler.feature_external_ges, 0)
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        parser.setFeature(xml.sax.handler.feature_external_pes, 0)

        parser.parse(self.xmlFile)
        return AlbumData(reader.getResult(), self.xmlFileDir)


    def maybeLoadFromXML(self, conf):
        '''
        Maybe we should add a param to force reparsing from disk
        '''
        if self.parsed:
            return self.xmlData
        
        logger.info('Parsing %s' % self.xmlFileName)

        # can we use the cached xml content ?
        # try to load our stuff from the cache if the xml wasn't modified
        cached = conf.canUseCache(self.xmlFileName)
        
        if cached:
            pickleFd = open(conf.pickleFilename)
            self.xmlData = load(pickleFd)
        else:
            self.xmlData = self.parse()
            # I cant remember what this line does ...
            self.xmlData.libraryPath = self.xmlFileDir
            
            # writing the cached data to a file
            # (shouldn't we do that only the first time ?)
            logger.info('writing the cached data in %s' % conf.pickleFilename)
            pickleFd = open(conf.pickleFilename, 'w')
            dump(self.xmlData, pickleFd)
        
        pickleFd.close()
        logger.info("\t[DONE]\n")

        self.parsed = True
        return self.xmlData


# Code snipets kept for memory

# 2005-08-08T06:03:54Z
# Format used by old Panther iPhoto version 2
# %V and %F should be enough according to
# strftime man page
# gave up with strptime ... using regexp instead
# self.value = time.strptime(val, '%y-%m-%d-T%TZ')

# import re, datetime
# T = re.compile('(\d*)-(\d*)-(\d*)T(\d*):(\d*):(\d*)Z').findall(val)[0]
# tup = tuple ([ int(i) for i in T ])
# self.value = datetime.datetime(*tup)
            
