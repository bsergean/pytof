"""
Class used to initiate a ftp connection to a remote ftp server,
and push the output of a pytof session there (or any directory).

Still in alpha.

Working (a bit ...) with:
    - Mandriva 2007 proftpd
    - Solaris 8 default ftp server

Not working with:
    - Apple OSX
    - free.fr ftpperso ftp server

We tried to use a ftpd python server (see tools/ftpd),
but it did not implement the whole ftp protocol.
"""

# Copyright (C) 2006, 2007 GPL
# Written by Benjamin Sergeant <bsergean@gmail.com>

__revision__ = '$Id$  (C) 2007 GPL'

from log import logger
from os.path import join, basename, isabs
from os import listdir, lstat
from stat import S_ISDIR, S_ISLNK
from utils import notYetImplemented
from ftplib import FTP, error_temp, all_errors
from getpass import getuser, getpass

class ftpUploader(FTP):
    '''
    For the ftplib manual see http://docs.python.org/lib/ftp-objects.html
    For ftp commands explanations see http://www.nsftools.com/tips/RawFTP.htm
    '''

    def __init__(self, host, user, password, port=21):
        ''' Start the connection '''
        self.ok = False
        try:
            FTP.__init__(self)
            self.set_debuglevel(2)
            
            logger.debug('host (%s) port (%s)' % (host, port))
            self.connect(host, port)
            self.login(user, password)
            self.ok = True
        except all_errors, msg:
            logger.error(msg)

    def infos(self):
        if not self.ok: return
        logger.info('Remote current ftp identification: %s' % self.getwelcome())

    def exists(self, fn):
        ''' Test whether file exist '''
        if not self.ok: return
        logger.debug('Does %s exists' % fn)
        try:
            lines = []
            def callback(line): lines.append(line)
            self.dir('-a %s' % fn, callback)
            logger.debug(lines)
            if len(lines) and 'No such file or directory' in lines[0]:
                return False
            return True
        except error_temp:
            return False

    def upload(self, src, tget = None):
        ''' Caution: no error handling '''
        if not self.ok: return
        fd = open(src)
        # be carefull to leave a space between STOR and the filename
        if not tget:
            tget = basename(src)
        self.storbinary('STOR ' + tget, fd)
        fd.close()

    def lsdir(self, path):
        '''
        List files within the "path" directory
        We use the non-standard -a to get filename
        starting with a dot (like .bashrc)
        '''
        if not self.ok: return
        logger.debug('lsdir %s' % path)

        lines = []
        def callback(line):
            lines.append(line)

        self.dir('-a %s' % path, callback)

        files = []
        for l in lines:
            # need to do a better job here since there
            # may be a problem with file containing whitespace
            logger.debug('Current line: %s' % l)
            if l.startswith('total'):
                continue
            
            fn = l.split()[8]
            logger.debug('Current token: %s' % fn)
            
            if l.startswith('d'):
                if fn != '.' and fn != '..':
                    files.append( (fn, 'Directory') )
            elif l.startswith('l'):
                files.append( (fn, 'Symbolic link') )                
            else:
                files.append( (fn, 'Regular File') )

        return files

    def rmtree(self, path):
        if not self.ok: return
        if not self.exists(path): return
        self.rmtree_r(path)
        
    def rmtree_r(self, path):
        '''
        Caution: This method depends on lsdir which may be buggy (symlinks)
        Recursive, inspired from shutil.rmtree
        '''
        if not self.ok: return
        files = self.lsdir(path)
        logger.debug(files)

        for f, fileType in files:
            fullpath = join(path, f)

            if fileType == 'Directory':
                logger.info('recurse on %s' % fullpath)
                self.rmtree_r(fullpath)
            elif fileType == 'Regular File':
                logger.info('remove file %s' % fullpath)
                self.delete(fullpath)
            else:
                logger.error('Unknown file type !!')

        if self.exists(path):
            logger.info('remove dir %s' % path)
            self.rmd(path)

    def cp_rf(self, src, tget):
        if not self.ok: return
        src_basename = basename(src)
        full_tget = join(tget, src_basename)
        self.rmtree(full_tget)
        self.mkd(full_tget)
        self.mirror_r(src, full_tget)

    def mirror_r(self, src, tget):
        ''' Recursive version '''
        if not self.ok: return
        names = listdir(src)
        logger.debug(names)

        for name in names:
            fullname = join(src, name)
            r_fullname = join(tget, name)
            try:
                mode = lstat(fullname).st_mode
            except: pass
            if S_ISDIR(mode):
                self.mkd(r_fullname)
                self.mirror_r(fullname, r_fullname)
            elif S_ISLNK(mode):
                # FIXME
                #notYetImplemented()
                pass
            else:
                self.upload(fullname, r_fullname)

def getStringFromConsole(text, default = ''):
    value = raw_input('%s[%s]:' %(text, default))
    if not value:
        return default
    return value

def ftpPush(conf, archive, topDir, fs):
    logger.debug('Entering ftp code')
    fromConfig = False
    if conf.hasFtpParams():
        answer = getStringFromConsole('Use last ftp parameters', 'y')
        if answer == 'y':
            host, user, passwd, remoteDir = conf.getFtpParams()
            fromConfig = True        

    if not fromConfig:
        # localhost is a preference for test
        host = getStringFromConsole('Host', 'localhost')
        user = getStringFromConsole('User', getuser())
        passwd = getpass()
        remoteDir = getStringFromConsole('Remote directory', '')
        if not isabs(remoteDir):
            logger.warning('Sorry: the remote drectory has to be an absolute path')
            remoteDir = ''

    try:
        ftpU = ftpUploader(host, user, passwd)
    except (error_perm):
        logger.error('Incorrect ftp credentials')
        sys.exit(1)

    if not ftpU.ok:
        logger.error('Connection failed')
        sys.exit(1)               
                
    if remoteDir:
        if not ftpU.exists(remoteDir):
            logger.info('remote dir %s does not exist' % remoteDir)
            remoteDir = ftpU.pwd()
    else:
        remoteDir = ftpU.pwd()
    conf.setFtpParams(host, user, passwd, remoteDir)
                
    if archive:
        logger.info('upload archive')
        ftpU.upload(archive,
                    join(remoteDir, basename(archive)))
    else:
        # we'll have to mirror the whole dir

	# A single file upload sample 
	# (to be used for pytof/index.html for example)
	# ftpU.upload('myfile',
	#	    join(remoteDir, basename(cssfile)))
        ftpU.cp_rf(topDir,
                   remoteDir)
