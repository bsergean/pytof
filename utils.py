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

import sys
import os

def echo(s):
    sys.stdout.write(s)
    sys.stdout.flush()

def _err_exit(msg):
    """ to exit from program on an error with a formated message """
    sys.stderr.write("%s: %s\n" % (os.path.basename(sys.argv[0]), msg))
    sys.exit(1)

def _err_(msg):
    """ print a formated message on error """
    sys.stderr.write("%s: %s\n" % (os.path.basename(sys.argv[0]), msg))

def posixpath(d):
    """
from bash man page :
       metacharacter
              A character that, when unquoted, separates words.   One  of  the
              following:
              |  & ; ( ) < > space tab
       control operator
              A token that performs a control function.  It is one of the fol-
              lowing symbols:
              || & && ; ;; ( ) | <newline>

So all these characters should be backslashed
    """
    printDir = d
    SpecificChars =    [' ' , '\''  , '(' , ')' , '&' , ';' , '|' , '<' , '<' ]
    SpecificNewChars = ['\ ', '\\\'', '\(', '\)', '\&', '\;', '\|', '\<', '\>']

    for o, n in zip(SpecificChars, SpecificNewChars): # o = old, n = new
        printDir = printDir.replace(o, n)

    return printDir

def bashableString(str):
    """ for string that aren't path """
    return posixpath(str)

def RemoveSpecificChars(string):
    """ Remove parenthesis and special chars from a string
    (when making freeDB request) """
    SpecificChars =    [' ' , '\''  , '(' , ')' , '&' , ';' , '|' , '<' , '<' ]
    for o in SpecificChars:
        string = string.replace(o, '')
    return string

def RemoveAccents(string, lfd, report = True):
    """ Remove accents chars from a string
    (when making freeDB request) """
    CleanString = string
    SpecificChars =    ['\xe9', '\xe8', '\xea', '\xe0', '\xf9']
    SpecificNewChars = ['e', 'e', 'e', 'a', 'u']
    SomethingReplaced = False

    for o, n in zip(SpecificChars, SpecificNewChars): # o = old, n = new
        CleanString = CleanString.replace(o, n)
        if o in string:
            SomethingReplaced = True

    if SomethingReplaced and report:
        lfd.write(string + ' -> ' + CleanString + '\n')

    return CleanString

def GetLonguestFileTitle(file_list):
    """ get the longuest string from a list """
    return max([len(i) for i in file_list])

def GetTmpFileDescriptorAndFileName():
    """ get a tmp filename descriptor """
    import tempfile
    filename = tempfile.mkstemp()[1]
    filedescriptor = open(filename, 'w')
    return filedescriptor, filename 


def ListCurrentDirFileFromExt(ext):
    """ list file matching extension from a list
    in the current directory
    emulate a `ls *.{(',').join(ext)` with ext in both upper and downcase}"""
    import glob
    extfiles = []
    for e in ext:
        extfiles.extend(glob.glob('*' + e))
        extfiles.extend(glob.glob('*' + e.swapcase()))

    return extfiles

pytof_modules = {
    'Image' : """
Python imaging library module missing : 
see http://code.google.com/p/pytof/wiki/Install
""",
    'dummyModule' : """
dummyModule missing : 
see http://...
"""

    }

def TryToImport(modules):
    """ try to import modules from a list """
    for mod in modules:
        try:
            exec 'import '+ mod
        except (ImportError):
            print pytof_modules[mod]
            sys.exit(1)

def help(str, revision, dependencies, author):
    """ print a nice page (which is the actual man page too) """

    # extract miscutils from a rcs id like
    # $Id$  (C) 2004 GPL'
    print str % (revision.split()[1].split(',')[0].split('.')[0])
    print """
VERSION
        %s
        
DEPENDENCIES
        %s

AUTHOR
        %s
"""  % (revision.split()[2],   
        (', ').join(dependencies),
        author)

class BadYear: pass
def CorrectYear(year):
    """ A year for music is correct if it is between now and 1500 """
    import datetime
    JC_music = 1500
    try:
        y = int(year)
        if y < JC_music or y > datetime.datetime.now().year:
            raise BadYear
    except (ValueError):
        raise BadYear

## useless but kept for memory
class BadMusicDirectoryName: pass
def GetArtistAndAlbumFromMusicDirectoryName(dir = None):
    """ A dir for music is correct if it is of the form :
    /<Artist>/<Artist> - <Album>/
    """
    if not dir:
        dir = os.getcwd()
    dir = os.path.abspath(dir)
    if not '-' in dir:
        raise BadMusicDirectoryName

    ArtistAndAlbum = os.path.basename(dir)
    Artist = os.path.basename(os.path.dirname(dir))

    if Artist != ArtistAndAlbum[0:len(Artist)]:
        raise BadMusicDirectoryName

    Album = ArtistAndAlbum[len(Artist)+3:]

    return Artist, Album

# see http://www.nedbatchelder.com/blog/200410.html#e20041003T074926
def _functionId(nFramesUp):
        """ Create a string naming the function n frames up on the stack.
        """
        co = sys._getframe(nFramesUp+1).f_code
        return "%s (%s @ %d)" % (co.co_name, co.co_filename, co.co_firstlineno)

def notYetImplemented():
        """ Call this function to indicate that a method isn't implemented yet.
        """
        raise Exception("Not yet implemented: %s" % _functionId(1))

def complicatedFunctionFromTheFuture():
        notYetImplemented()
        
outfd = sys.stderr
outfd = open('/tmp/message', 'w')
def log(msg):
        # we have to cast some type ('instance',
        # the error message from an exception), to print it
        outfd.write(str(msg) + '\n')
        outfd.flush()


if __name__ == "__main__":
    # FIXME : Add tests here
    print posixpath('/mnt/data/mp3/Red Hot Chili Peppers/Red Hot Chili Peppers - Blood Sugar Sex Magik/08 - The Righteous & The Wicked.mp3')

    Years = ['caca', 1492, 2078, 1999, '\n']
    for y in Years:
        sys.stdout.write(str(y) + ' : ')
        try:
            year = CorrectYear(y)
        except(BadYear):
            print "BadYear"
            continue
        print "(pneux) GoodYear"

    Dirs = [ ['U2','U2 - Achtung Baby'] , ['U2','U2 Achtung Baby']]
    for d in Dirs:
        fakedir = '/tmp/' + d[0] + '/' + d[1]
        os.system('mkdir -p ' + posixpath(fakedir))
        print 'Sample Dir :', fakedir
        try:
            Artist, Album = GetArtistAndAlbumFromMusicDirectoryName(fakedir)
            print '\tArtist :', Artist
            print '\tAlbum :', Album
            print '\tOK'
        except(BadMusicDirectoryName):
            print '\tBadMusicDirectoryName raised'
        

    # FIXME: add a test for GetTmpFileDescriptorAndFileName

    # custom import test
    __dependencies__ = ['dummyModule']

    TryToImport(__dependencies__)
    for mod in __dependencies__:
        exec 'import ' + mod
