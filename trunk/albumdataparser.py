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

from os.path import expanduser, exists, join
from xml.parsers.expat import ParserCreate, ExpatError
from photo import Photo
from utils import _err_, _err_exit, log

class AlbumData(object):
    def __init__(self, data):
        self.data = data

    def getAlbumByName(self, name):
        for album in self.data['List of Albums']:
            if album['AlbumName'] == name:
                return album
        raise Error, "Album \"%s\" not in iPhoto Library" % name

    def getPicturePathFromId(self, id):
        return self.data['Master Image List'][id]['ImagePath']

    def getPicturesIdFromAlbumName(self, name):
        res = []
        album = self.getAlbumByName(name)
        return album['KeyList']

    def getPhotoFromId(self, id):
        p = self.data['Master Image List'][id]
        return Photo(p['ImagePath'],
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
        else:
            raise ExpatError, "Type \"%s\" not supported" % type

class AlbumDataParserError: pass
class AlbumDataParser(object):
    def __init__(self, xmlFileName=expanduser('~/Pictures/iPhoto Library/AlbumData.xml')):

        self.error = False
        if not exists(xmlFileName):
            raise AlbumDataParserError

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
            elif name in ['key', 'string', 'integer', 'real', 'true', 'false']:
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
            elif name in ['key', 'string', 'integer', 'real', 'true', 'false']:
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


def infos(albumName, libraryPath):
    """
    FIXME: try to do something with albumName
    """
    log("Parsing AlbumData.xml")
    if not libraryPath:
        libraryPath = expanduser('~/Pictures/iPhoto Library')
    xmlFileName = join(libraryPath, 'AlbumData.xml')

    try:
        parser = AlbumDataParser(xmlFileName)
        data = parser.parse()
    except(AlbumDataParserError):
        _err_exit("Problem parsing AlbumData.xml")
    

if __name__ == '__main__':
    adp = AlbumDataParser()
    data = adp.parse()
    alb = data.getAlbumByName("Test")
    print alb['Album Type']
    print alb['KeyList']
    print
    for f in data.getPictureFilesFromAlbumName('Test'):
        print f
