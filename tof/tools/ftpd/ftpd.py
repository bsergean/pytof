# ftpd.py   Simple FTP server, re-implemented from FTPserver.java
#	Peter Harris 18-9-2000
#	For FTP specification, see RFC959 (http://www.faqs.org/rfcs/rfc959.html)
#
# Copyright (C) 2002 Peter Harris and Kyndal International
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#

# version 0.1 - 5 Nov 2001 - first working version
# version 0.2 - 8 Nov 2001 - Fixed NLST to glob wildcards
# version 0.3 - 22 Nov 2001 - Different set of default allowed filename extensions
# version 0.4 - 21 Jan 2002 - do no CRLF translation on RETR in ascii mode.
# version 0.5 - 16 Dec 2002 - start in binary mode by default
#   Refactoring out filesystem code so you can make an FTP server that serves
#   a virtual directory structure instead.
# version 0.6 - 8 Jan 2003 - catch error when opening file for STOR
# version 0.7 - 10 Jan 2003 - bugs in NLST and RETR fixed
# version 0.8 - 10 Jan 2003 - implemented DELE in FileFTPSession
from socket import *
import SocketServer
import sys, os, string
from glob import glob1      #(0.2)
from options import options # parses command line options the way I like

# initial values
version="0.8"
version_date="10-1-2003"

# ----------------------------------------------------------------------------
# FTP session class

class FTPsession(SocketServer.BaseRequestHandler):
    """One FTP Session from login to exit"""
    def setup(self):
        self.binary = 1         # starts in binary mode
        self.datasocket = None  # Data socket
        try:
            self.options = self.server.options  # customisation
        except:
            self.options = {}
        self.base_dir = self.basedir()
        self.current_dir = self.base_dir
        self.lookup = \
        { "syst":self.syst,
          "user":self.user,
          "pass":self.passwd,
          "rein":self.rein,
          "type":self.type,
          "noop":self.noop,
          "mode":self.mode,
          "stru":self.stru,
          "port":self.port,
          "site":self.site,
          "stor":self.stor,
          "retr":self.retr,
          "list":self.list,
          "nlst":self.nlst,
          "cdup":self.cdup,
          "cwd":self.cwd,
          "dele":self.dele,
          "pwd":self.pwd,
        }

    def response(self,s):
        """Send a response to the client"""
        self.request.send("%s\n" % s)
        self.echo(s)

    # Define methods, one per FTP command as described in RFC959
    def syst(self,args):
        """System Info"""
        self.response("215 Python FTPserver %s" % version)


    def user(self,args):
        """User login"""
        if args[0] != "anonymous":
            self.response("502 Only anonymous user implemented")
        else:
            self.response("230 OK, password not required")
            self.binary = 0
            self.current_dir = self.base_dir


    def passwd(self,args):
        """Password"""
        self.response("230 OK, password ignored")


    def rein(self,args):
        """Re-initilaise session state"""
        self.response("200 Using binary mode for transfers")
        self.binary=1
        self.current_dir=self.base_dir

    def type(self,args):
        """Set type of transfer, I=binary, A=ASCII"""
        try:
            t=string.lower(args[0])
            if t not in ["a","i"]:
                self.response("501 type %s not implemented" % t)
            else:
                self.binary=(t == "i")
                self.response("200 type %s" % t)
        except:
            self.response("500 type syntax")

    def noop(self,args):
        self.response("200 ")

    def mode(self,args):
        """Obscure FTP thing, rarely used"""
        try:
            m=string.lower(args[0])
            if m != "s":
                self.response("501 mode %s not implemented" % m)
        except:
            self.response("500 mode syntax")

    def stru(self,args):
        """Another obscure FTP thing, rarely used"""
        try:
           s=string.lower(args[0])
           if s != "f":
               self.response("501 stru %s not implemented" % s)
        except:
           self.response("500 stru syntax")

    def port(self,args):
        try:
            nums=string.split(args[0],',')
            if self.datasocket:
                self.datasocket.close()
                self.datasocket=None
            portnum=int(nums[4])*256 + int(nums[5])
            host=string.join(nums[0:4],".")
            self.datasocket=socket(AF_INET,SOCK_STREAM)
            self.datasocket.connect((host,portnum))
            self.response("200 port %d of %s" % (portnum, host))
        except IndexError:
            self.response("500 port syntax")

    def site(self,args):
        self.response("502 site not implemented")
    

    def list(self,args):
        self.nlst(args) # stub implementation - just the names

    def canSee(self,path):
        """Determine whether absolute path is inside base directory"""
        return os.path.abspath(path)[:len(self.base_dir)] == self.base_dir            
    
    def cdup(self,args):
        if self.current_dir != self.base_dir:
            self.current_dir = os.path.split(self.current_dir)[0]
            self.response("200 Now in %s" % self.current_dir)
        else:
            self.response("553 Already at base directory")

    def isdir(self,pathname):
        """Is pathname a directory"""
        return 0    # Override this

    def basedir(self):
        """Return base directory of server"""
        return ""   # Override this
    
    def stor(self,args):
        """Store a file"""
        self.response("502 STOR not implemented")   # Override this

    def retr_data(self,filename):
        """Get the data from a file, if it exists"""
        return None # Override this

    def retr(self,args):
        if args:
            fname = args[0]
            data = self.retr_data(fname)
            if data is not None:
                bytes = len(data)
                self.response("125 Data transfer starting")
                self.datasocket.send(data)
                self.datasocket.close()
                self.datasocket = None
                self.response("226 Closing data connection, sent %d bytes" % bytes)
            else:
                self.response("553 filename not allowed")
        else:
            self.response("500 retr syntax")

    def nlst_data(self,dirname):
        """Get a list of file names from a directory, if it exists"""
        return None # Override this
    
    def nlst(self,args):
        if args:
            tail = args[0]
        else:
            tail = "."
        lst = self.nlst_data(tail)
        if lst is not None:
            self.response("150 opening ASCII connection for file list")
            data = "\r\n".join(lst+[''])
            self.datasocket.send(data)
            self.datasocket.close()
            self.response("226 transfer complete")
        else:
            self.response("553 outside base directory of server")

        
    def cwd(self,args):
        try:
            dirarg=args[0]
        except:
            dirarg='/'

        newdir = self.absolute_path(dirarg)

        if self.canSee(newdir):
            if self.isdir(newdir):
                self.current_dir = newdir
                self.response("200 Now in %s" % self.current_dir)
            else:
                self.response("550 Directory not found")
        else:
            self.response("553 Pathname outside base directory")

    def dele(self,args):
        """Delete a file"""
        self.response("502 DELE not implemented")   # Override this
            

    def pwd(self,args):
        self.response("257 /tmp")

    def absolute_path(self,fname):
        joindir=self.current_dir
        if fname[0] == '/' or fname[0] == '\\':
            fname=fname[1:]
            joindir=self.base_dir
        return os.path.join(joindir,fname)
    
    def echo(self,message):
        """override this to (for example) log to a file"""
        print message

    def handle(self):
        self.peername = self.request.getpeername()
        self.response("220 Python FTPserver %s (P Harris %s) Ready" % (version,version_date))
        while 1:
            command_line=self.request.recv(1024)
            if (not command_line): break  # connection closed at client end?
            command_split = string.split(command_line)
            command = string.lower(command_split[0])
            self.echo("%s:%s" % (self.peername, command_line))
            if command == "quit":
                self.response("221 OK, bye")
                break
            # Do what the command asks, if there is a method to do it.
            if self.lookup.has_key(command):
                try:
                    self.lookup[command](command_split[1:])
                except:
                    self.response("451 Requested action aborted; local error")
                    raise # throw it again, need to see the traceback
            else:
                self.response("502 %s not implemented" % command)
        
class FileFTPsession(FTPsession):
    """An FTP session that is really serving files from the file system"""
    def isdir(self,pathname):
        return os.path.isdir(pathname)

    def basedir(self):
        return os.path.abspath(self.options.get('dir','.'))
    
    def stor(self,args):
        if args:
            fname = args[0]
            pathname=self.absolute_path(fname)
            if self.canSee(pathname) and not os.path.isdir(pathname):
                #mode = ['w','wb'][self.binary]
                try:
                    fout = open(pathname,'wb') # check if this is OK
                    bytes = 0
                    self.response("125 Data transfer starting")
                    try:
                        while 1:
                            data = self.datasocket.recv(1024)
                            bytes = bytes + len(data)
                            if not data: break
                            fout.write(data)
                    except:
                        pass
                    fout.close()
                    self.response("200 OK, received %d bytes" % bytes)
                except:
                    self.response("451 Requested action aborted; local error")
            else:
                self.response("553 filename not allowed")
        else:
            self.response("500 stor syntax")            

    def retr_data(self,filename):
        pathname=self.absolute_path(filename)
        if self.canSee(pathname) and os.path.isfile(pathname):
            data = open(pathname,'rb').read()
        else:
            data = None
        return data
        

    def nlst_data(self,dirname):
        dirname = self.absolute_path(dirname)
        if self.canSee(dirname):
            if os.path.isdir(dirname):
                lst = os.listdir(dirname)
            else: #(0.2)
                dirname,pattern=os.path.split(dirname)
                lst = glob1(dirname,pattern)
        else:
            lst = None
        return lst
            
    def dele(self,args):
        if args:
            fname = args[0]
            pathname=self.absolute_path(fname)
            if self.canSee(pathname):
                try:
                    if os.path.isdir(pathname):
                        os.rmdir(pathname)
                    else:
                        os.remove(pathname)
                    self.response("200 OK, deleted %s" % fname)
                except:
                    self.response("451 Requested action aborted; local error")
            else:
                self.response("553 filename not allowed")
        else:
            self.response("500 DELE syntax")            
        
    
class DangerousFTPsession(FileFTPsession):
    def site(self,args):
        if len(args) == 2 and args[0] == 'start':
            pathname=self.absolute_path(args[1])
            base,ext=os.path.splitext(pathname)
            default_allow=['.txt']
            allowed=self.options.get('allow',default_allow)
            if self.canSee(pathname) and ext in allowed:
                os.system("start %s" % pathname)
                self.response("200 OK")
            else:
                self.response("553 filename not allowed")
        else:
            self.response("500 site syntax: site start filename")

class NotifyingFTPsession(FileFTPsession):
    """The site command calls back to 'callback' specified in options.
    The return value should be a valid FTP response, or else None.
    """
    def site(self,args):
        callback=self.options.get('callback',None)
        if callback:
            try:
                response=callback(args)
                if not response or response[0] not in ['2','4','5']:
                    self.response("200 OK")
                else: self.response(response)
            except:
                self.response("451 Requested action aborted; local error")
        else:
            self.response("502 site not implemented")
            
class FTPserver(SocketServer.ThreadingTCPServer):
    def __init__(self,bind_to=('',21),handler=FTPsession,**options):
        self.options = options
        SocketServer.ThreadingTCPServer.__init__(self,bind_to,handler)
    def verify_request(self,reqsocket,client_address):
        hosts = map(gethostbyname,self.options.get('hosts',[]))
        if hosts and client_address[0] not in hosts:
            print "Hosts allowed:",hosts
            print "Rejecting connection from", client_address[0]
            return 0
        else: return 1

# MAIN ------------------------------------------------------------------------
if __name__ == '__main__':
    syntax={'--port':'21','--hosts':[],'--start':0,'--dir':'.',
            '--allow':('.txt','.ux','.csv','.doc','.html','.rtf'),
            '--allow-also':[],
            '--help':0,'--once':0}
    opts=options(syntax,sys.argv[1:])
    try:
        hosts = opts['--hosts']
        start = opts['--start']
        base = opts['--dir']
        allow = list(opts['--allow']) + opts['--allow-also']
        port = int(opts['--port'])
        once = opts['--once']
        help = opts['--help']
    except:
        port = 21
        start = 0
        base = '.'
        hosts = []
        allow = ['.txt']
        once = 0
        help = 0

    print "Python ftpd", version, version_date, " Peter Harris (--help for help)" 
    if help:
        print "--help   : see this message"
        print "--port P : run on port P (default is 21)"
        print "--hosts H1,H2,... : set hosts allowed to connect"
        print "--dir D  : downloads are in directory D (default is current)"
        print "--start  : can start applications to open files"
        print "--allow E1,E2,... : allowed file extensions for --start"
        print "--allow-also E1,E2,... : add to default allowed extensions instead of replacing"
        print "--once   : serve one session then exit"
        wait=raw_input('Press a key...')
    else:
        handler=(FileFTPsession,DangerousFTPsession)[start]
        server = FTPserver(bind_to=('',port),
                       handler=handler,
                       hosts=hosts,dir=base,allow=allow)
        if once:
            server.handle_request()
            wait=raw_input('Press a key...')
        else:
            server.serve_forever()
