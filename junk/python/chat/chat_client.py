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
            url = self.urlbase + 'up'
            urlopen(url)
        except (IOError):
            self.ok = False

    # Server request:
    def get_all(self, user, index):

        url = self.urlbase + 'all' + '?'
        fmt = ''
        fmt += 'user=%s&'
        fmt += 'index=%d&'
        args = fmt % (
                urlsafe_b64encode(user),
                index)
        url += args

        data = urlopen(url).read()
        if data != 'Empty' and data != 'internal server error':
            i, dummy, text = data.partition('\n')
            stdout.write('\r' + text + '\n')
            return int(i)
        else:
            return None

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
        index = 0

        while not self.quit:
            ret = cc.get_all(user, index)
            if ret:
                index = ret + 1
                stdout.write(user + '> ')
                stdout.flush()
            sleep(1)

class ChatInterpreter():

    def __init__(self, cc, user):
        self.cc = cc
        self.user = user

    def loop(self):

        # The writting thread
        self.t = MyThread()
        self.t.start()

        # Display first prompt
        stdout.write(self.user + '> ')

        while True:
            try:
                text = raw_input()
                stdout.write(self.user + '> ')
                stdout.flush()
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
    parser.add_option("-l", "--username", dest="user", default=getuser(),
            help="Your user name")
    options, args = parser.parse_args()
    user = options.user
    host = options.host

    # Start
    cc = ChatClient(host)
    if not cc.ok:
        print 'Chat server down'
        exit(1)

    ci = ChatInterpreter(cc, options.user)
    ci.loop()
    ci.t.quit = True

# vim: set tabstop=4 shiftwidth=4 expandtab :
