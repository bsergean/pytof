#!/usr/bin/env python

from urllib import urlopen
from time import sleep
from sys import argv, stdout, exit
from getpass import getuser
from time import time
from base64 import urlsafe_b64encode
from threading import Thread
from optparse import OptionParser
from os import linesep

class ChatClient:
    def __init__(self, server_host):
        if server_host == None:
            self.server_host = 'localhost'
        else:  
            self.server_host = server_host

        port = '8080'
        self.urlbase = 'http://' + self.server_host + ':' + port + '/' 

        self.ok = True
        try:
            url = self.urlbase + 'status'
            urlopen(url)
        except (IOError):
            self.ok = False

    # Server request:
    def get_all(self, ts, user):

        url = self.urlbase + 'all' + '?'
        fmt = ''
        fmt += 'ts=%s&'
        fmt += 'user=%s&'
        args = fmt % (
                urlsafe_b64encode(str(ts)), 
                urlsafe_b64encode(user))
        url += args

        data = urlopen(url).read()
        if data != 'Empty':
            stdout.write('\r' + data + '\n')
            return True
        else:
            return False

    # Server request:
    def send_text(self, text, user):

        url = self.urlbase + 'set_msg' + '?'
        fmt = ''
        fmt += 'msg=%s&'
        fmt += 'user=%s&'
        args = fmt % (
                urlsafe_b64encode(text), 
                user)
        url += args
        data = urlopen(url).read()

# Update screen every seconds with what friends are writting (or nothing)
class MyThread(Thread):

    def run(self):

        global user

        # We need self.quit to stop the program
        # by setting it to True
        self.quit = False 
        ts = time()

        while not self.quit:
            sleep(2)
            if cc.get_all(ts, user):
                ts = time()
                stdout.write(user + '> ')
                stdout.flush()

class ChatInterpreter():

    def __init__(self, cc, user):
        self.cc = cc
        self.user = user

    def loop(self):

        # Print what has been written up until now
        print self.user
        self.cc.get_all(0, self.user)

        # The writting thread
        self.t = MyThread()
        self.t.start()

        while True:
            stdout.write(self.user + '> ')
            try:
                text = raw_input()
            except(EOFError,KeyboardInterrupt): # Bye bye
                print
                return

            if text:
                self.cc.send_text(text, self.user)

if __name__ == "__main__": 
    
    # parse args
    parser = OptionParser(usage = "usage: %prog <options>")

    host = None
    user = ''
    parser.add_option("-s", "--host", dest="host",
            help="The host plus port number where the server is running")
    parser.add_option("-u", "--user", dest="user", default=getuser(),
            help="Your user name")
    options, args = parser.parse_args()
    user = options.user

    # Start
    cc = ChatClient(host)
    if not cc.ok:
        print 'Chat server down'
        exit(1)

    ci = ChatInterpreter(cc, options.user)
    ci.loop()
    ci.t.quit = True

# vim: set tabstop=4 shiftwidth=4 expandtab :
