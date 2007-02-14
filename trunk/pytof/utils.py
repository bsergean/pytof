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
from os.path import splitext, expanduser, join, exists, basename, walk, isfile
import tarfile
from zipfile import ZipFile, ZIP_DEFLATED
from log import logger

sys.path.insert(1, '../deps/ftputil-2.2')

def echo(s):
    sys.stdout.write(str(s) + '\n')
    sys.stdout.flush()

def _err_exit(msg):
    """ to exit from program on an error with a formated message """
    _err_(msg)
    sys.exit(1)

def _err_(msg):
    """ print a formated message on error """
    sys.stderr.write("%s: %s\n" % (os.path.basename(sys.argv[0]), msg))

def maybemakedirs(path):
    if not exists(path):
        os.makedirs(path)

def urlExtractor(htmlpage):

    html = open(htmlpage).read()

    urls = []
    import re
    url = unicode(r"((http|ftp)://)?(((([\d]+\.)+){3}[\d]+(/[\w./]+)?)|([a-z]\w*((\.\w+)+){2,})([/][\w.~]*)*)")
    for m in re.finditer(url, html) :
        urls.append(m.group())

    return urls

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

def GetTmpDir():
    """ get the os tmp dir """
    from tempfile import mktemp
    import tempfile # FIXME: is there a way to get tempdir value
    # without import tempfile ?
    # mktemp has to be called once for tempdir to be initalized !!
    mktemp()
    return tempfile.tempdir

def ListCurrentDirFileFromExt(ext, path):
    """ list file matching extension from a list
    in the current directory
    emulate a `ls *.{(',').join(ext)` with ext in both upper and downcase}"""
    import glob
    extfiles = []
    for e in ext:
        extfiles.extend(glob.glob(join(path,'*' + e)))
        extfiles.extend(glob.glob(join(path,'*' + e.swapcase())))

    return extfiles

def UnixFind(dir, ext):
    '''
    return a flatened list of files with a specific extension
    '''
    found = []
    for dummy1, dummy2, files in os.walk(dir):
        found.extend([i for i in files if splitext(i)[1] == ext])

    return found


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
    for module in modules:
        try:
            exec 'import '+ module
        except (ImportError):
            print pytof_modules[module]
            sys.exit(1)

def automaticHelp(str, revision, dependencies, author):
    """
    print a nice page (which is the actual man page too)
    deprecated since we use the optparse class
    """

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

class BadYear(Exception): pass
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
class BadMusicDirectoryName(Exception): pass
def GetArtistAndAlbumFromMusicDirectoryName(directory = None):
    """ A dir for music is correct if it is of the form :
    /<Artist>/<Artist> - <Album>/
    """
    if not directory:
        directory = os.getcwd()
    directory = os.path.abspath(dir)
    if not '-' in directory:
        raise BadMusicDirectoryName

    ArtistAndAlbum = os.path.basename(directory)
    Artist = os.path.basename(os.path.dirname(directory))

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

class ProgressMsg(object):
    """ General purpose progress bar """
    def __init__(self, target, output=sys.stdout):
        self.output = output
        self.counter = 0
        self.target = target

    def Increment(self):
        if self.counter == 0:
            self.output.write("\n")
        self.counter += 1
        msg = "\r%.0f%% - (%d processed out of %d) " \
            % (100 * self.counter / float(self.target), self.counter, self.target)
        self.output.write(msg)
        if self.counter == self.target:
            self.output.write("\n")
        elif self.counter >= self.target:
            raise Exception, "Counter above limit"

def lpathstrip(prefix, path):
    '''
    '''
    result = path.replace(prefix, '', 1)
    if result.startswith(os.sep):
        result = result.lstrip(os.sep)

    return result

def create(file, content):
    '''
    $ echo content > file
    '''
    fd = open(file, 'w')
    fd.write(content)
    fd.close()

def mkarchive(fn, prefix, mainDir, files, Zip = True, tar = False):
    '''
    FIXME: maybe we could do as in mkzip to avoid the chdir(s)
    - fn is the archive filename
    - prefix is the dir where we cd before creating the archive
    - mainDir is the directory to archive within prefix
    - files is a list of file with an absolute path which
    will be put in the archive at the prefix level
    '''
    args = (fn, prefix, mainDir, files)
    if Zip:
        return mkzip(*args)
    if tar:
        return mktar(*args)

def mkzip(fn, prefix, mainDir, files):
    def visit (z, dirname, names):
        for name in names:
            path = os.path.normpath(os.path.join(dirname, name))
            if isfile(path):
                filenameInArchive = lpathstrip(prefix, path)
                z.write(path, filenameInArchive)
                logger.info("adding '%s'" % filenameInArchive)

    ext = '.zip'
    if not fn.endswith(ext): fn = fn + ext

    z = ZipFile(fn, "w", compression=ZIP_DEFLATED)
    walk(join(prefix, mainDir), visit, z)

    for f in files:
        z.write(f, basename(f))
                
    z.close()
    return fn

def mktar(fn, prefix, mainDir, files):
    '''
    The TarFile is created with modew, the simple tar file.
    We could add compression (w|gz or w|bz2) but it is useless
    since we are working on compressed image in pytof
    '''
    ext = '.tar'
    if not fn.endswith(ext): fn = fn + ext
    
    pwd = os.getcwd()
    os.chdir(prefix)
    tarball = tarfile.open(fn, 'w') 
    tarball.add(mainDir)
    os.chdir(pwd)
    for f in files:
        # FIXME: maybe pb here: see zip section
        tarball.add(f, basename(f))
    tarball.close()

    # need to shut this up during test suite execution
    return fn

def chmodwwdir(prefix):
    ''' ww is world writable '''
    def visit (z, dirname, names):
        for name in names:
            path = os.path.normpath(os.path.join(dirname, name))
            if isfile(path):
                os.chmod(path, 777)

    walk(prefix, visit, None)

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
