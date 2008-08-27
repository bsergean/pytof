#!/usr/bin/env python
''' Talk to your roku '''
# DONT FORGET THE \n in your telnet command !!!

import telnetlib
import time
from model import *

class RokuCommander():
    def __init__(self, 
                debug = False,
                interact = False, 
                usual_telnet = False, 
                ):
        rokuhost = 'soundbridge.local'
        
        # roco stands for Roku Connection on port 4444 it looks like we have a
        # default telnet session, with a prompt while on 5555, we get a ad hoc
        # rcp (roku control protocol) connection. We default to this one
        if usual_telnet:
            self.roco = telnetlib.Telnet(rokuhost, 4444)
            self.write('rcp\n')
        else:
            self.roco = telnetlib.Telnet(rokuhost, 5555)

        self.roco.read_until('roku: ready')
        if debug: self.roco.set_debuglevel(5)

        if interact: self.roco.interact()

        # Try to do a dummy connect
        self.list_servers()
        self.write('ServerConnect 0')

        # Say we want a partial list result style
        if False:
            self.write('SetListResultType partial')
            self.roco.read_until('OK')

    # helpers
    def write(self, cmd):
        self.roco.write(cmd + '\n')
    def read_until(self, msg):
        return self.roco.read_until(msg)
    def read_ok(self):
        return self.read_until('OK')

    def list_something(self, cmd):
        while True:
            self.write(cmd + '\n')
            # Result can be error or success (seriously ?)
            # Dont know why, but first request after a connection is always a
            # failure. 
            ret, z, text = self.roco.expect(['ListResultEnd',
                    'GenericError', 
                    'ErrorDisconnected'])

            if ret == 0: # index of GenericError
                tokens = [t[len(cmd)+2:] for t in text.splitlines()]
                # for t in text.splitlines(): print t[len(cmd)+2:]
                return tokens
            else:
                print 'Failed, retrying'

    # Talk to roku (plumbing)
    # Tested
    def list_servers(self):
        self.list_something('ListServers')

    def list_medias(self, list_cmd, index):
        result = self.list_something(list_cmd)
        if len(result) > index:
            return result[index:-1]
        return None

    def list_artists(self):
        return self.list_medias('ListArtists', 4)
    def list_albums(self):
        return self.list_medias('ListAlbums', 3)
    def list_songs(self):
        return self.list_medias('ListSongs', 3)

    def filter_by_artist(self, artist):
        self.write('SetBrowseFilterArtist ' + artist)
        self.read_ok()

    def filter_by_album(self, album):
        self.write('SetBrowseFilterAlbum ' + album)
        self.read_ok()

    # Untested
    def list_genres(self):
        self.list_something('ListGenres')

# Database setup
setup_all(True)

# Roku query
debug = True
debug = False
r = RokuCommander(debug)
artists = r.list_artists()
for ro_artist in artists: #[:20]:

    # Have a problem with an 10.000 Hz Air album
    # Whatever People Say I Am, Tha
    if ro_artist.capitalize() == 'Air': continue 

    db_artist = Artist(name = ro_artist)
    r.filter_by_artist(ro_artist)

    for ro_album in r.list_albums():

        db_album = Album(name = ro_album, artist = db_artist)
        r.filter_by_album(ro_album)

        songs = r.list_songs()

        print len(songs)
        if len(songs) > 100:
            print ro_album
            continue
        
        if songs == None: continue
        for ro_song in songs:
            
            db_song = Song(name = ro_song, album = db_album)

session.flush()
# print Song.query.all()
# print Artist.query.all()
# print Album.query.all()
