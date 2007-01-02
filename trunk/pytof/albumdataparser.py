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

import os
from os.path import expanduser, exists, join
from xml.parsers.expat import ParserCreate, ExpatError
from photo import Photo
from utils import _err_, _err_exit, log
from time import strptime

class AlbumDataError(Exception): pass
class AlbumData(object):
    def __init__(self, data):
        self.data = data
        self.libraryPath = ''

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
            if not a.endswith('Book'):
                albums.append( [int(album['PhotoCount']), a] )

        # to sort by date, we would have to compute the date mean of
        # an album ... so we sort by the bigger album for now
        albums.sort()
        return [album[1] for album in albums]

    def getPicturePathFromId(self, id):
        return self.data['Master Image List'][id]['ImagePath']

    def getPicturesIdFromAlbumName(self, name):
        res = []
        album = self.getAlbumByName(name)
        return album['KeyList']

    def getPhotoFromId(self, id):
        p = self.data['Master Image List'][id]
        photoFileName = p['ImagePath']

        if self.libraryPath:
            try:
                # FIXME:
                if 'Originals' in photoFileName:
                    index = photoFileName.index('Originals')
                    photoFileName = join(self.libraryPath, photoFileName[index:])
                else:
                    # iPhoto 2 (Panther)
                    suffix = photoFileName.split('iPhotoLibrary' + os.sep)[1]
                    photoFileName = join(self.libraryPath, suffix)
                    
            except (ValueError):
                # probably panther iPhoto, there is no Original in the filenam
                print self.libraryPath
                _err_exit('Internal Error: cannot handle %s' %(photoFileName))

            log(photoFileName)

        if not p.has_key('DateAsTimerInterval'):
            p['DateAsTimerInterval'] = ''
            
        return Photo(photoFileName,
                     id,
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
        photos = data.getPicturesIdFromAlbumName(name)
        for id in photos:
            print id

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

class AlbumDataParserError: pass
class AlbumDataParser(object):
    def __init__(self,
                 xmlFileDir,
                 xmlFileBaseName):
        if not xmlFileDir:
            xmlFileDir = expanduser('~/Pictures/iPhoto Library')
        if not xmlFileBaseName:
            xmlFileBaseName = 'AlbumData.xml'
    
        xmlFileName = join(xmlFileDir, xmlFileBaseName)
        if not exists(xmlFileName):
            _err_('\nNo xml file found at %s' %(xmlFileName))
            raise AlbumDataParserError

        self.xmlFileName = xmlFileName
        self.xmlFile = file(xmlFileName, 'r')
        self.elemList = []
        self.lastItemData = ''
        self.keys = []
        self.albumData = None        

    def addItem(self, item):
            list = self.elemList[-1]
            if str(list.__class__) == "<type 'dict'>":
                list[self.keys.pop()] = item
            elif str(list.__class__) == "<type 'list'>":
                list.append(item)
            else:
                raise ExpatError, list.__class__

    def parse(self):
        def start_element(name, attrs):
            if name == 'dict':
                elem = {}
            elif name in ['plist', 'array']:
                elem = []
            elif name in ['key', 'string', 'integer', 'real', 'true', 'false', 'date']:
                elem = XmlItem(name)
            else:
                raise ExpatError, "Element \"%s\" not supported" % name
            self.elemList.append(elem)

        def end_element(name):
            item = self.elemList.pop()
            if name == 'plist':
                self.albumData = AlbumData(item[0])
                assert(len(self.elemList) == 0)
            elif name == 'dict':
                self.addItem(item)
            elif name == 'array':
                self.addItem(item)
            elif name in ['key', 'string', 'integer', 'real', 'true', 'false', 'date']:
                item.setValue(self.lastItemData)
                if name == 'key':
                    self.keys.append(item.value)
                else:
                    self.addItem(item.value)
            else:
                raise ExpatError, "Element \"%s\" not supported" % name
            self.lastItemData = ''

        def char_data(data):
            if not data.startswith('\n') and not data.startswith('\t'):
                self.lastItemData += data

        p = ParserCreate()
        p.StartElementHandler = start_element
        p.EndElementHandler = end_element
        p.CharacterDataHandler = char_data
        p.ParseFile(self.xmlFile)
        return self.albumData
    

if __name__ == '__main__':
    adp = AlbumDataParser()
    data = adp.parse()
    alb = data.getAlbumByName("Test")
    print alb['Album Type']
    print alb['KeyList']
    print
    for f in data.getPictureFilesFromAlbumName('Test'):
        print f







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
            
