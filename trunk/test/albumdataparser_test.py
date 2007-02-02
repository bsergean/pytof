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

from config import configHandler
from os import remove
from unittest import TestCase
from log import quiet

from albumdataparser import AlbumDataParser
from os.path import join

quiet()

class TestConfigHandler(TestCase):

    albums = """
mes-vacances-postales
Slyine Boulevard
Alexis
Le matin
Mont Saint Helena
Mont Tamalpais
Berkeley
Les chats
Sur la route de Big Sur
foot piscine
Sacramento
Sonoma
dominique et denis
Santa Cruz
Anniversaire BenjBenj
Los Angeles
Frog Jump
Chez nous
Gastronomie
Lake Tahoe
Yosemite
Bruges - Belgique
maman
New York
France - Lyon
Hawaii
A&M
"""

    def setUp(self):
        self.xmlFilename = 'AlbumData_gnocchi.xml'
        self.libraryPath = 'data'
        
        parser = AlbumDataParser(self.libraryPath, self.xmlFilename)
        self.xmlData = parser.parse()
    
    def testAlbumNames(self):
        ''' TODO: try with album with non-ascii chars '''
        albumList = self.xmlData.getAlbumList()

        for album in self.albums.splitlines():
            album = album.strip()
            if album:
                self.assert_(album in albumList)

    def testAlbumDates(self):
        pass
