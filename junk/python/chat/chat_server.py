#!/usr/bin/env python

'''
Write user sent content to a file that is read at each request ...
We should lock it in set_msg when writting
'''

import web
from base64 import urlsafe_b64decode
from time import time
from os.path import exists

com_fn = 'chat_com'

urls = (
  '/set_msg', 'set_msg',
  '/up', 'up',
  '/all', 'all')

class up:
    def GET(self):
        return ''

class all:
    def GET(self):

        if not exists(com_fn): return 'Empty'

        d = web.input()
        timestamp = urlsafe_b64decode(d.ts)
        user      = urlsafe_b64decode(d.user)

        text = []
        for l in open(com_fn).read().splitlines():
            tokens = l.split(',')

            db_timestamp = tokens[0]
            db_user      = tokens[1]
            msg          = urlsafe_b64decode(tokens[2])

            if msg and db_timestamp > timestamp and db_user != user:
                text.append(db_user + '> ' + msg)

        if not len(text): return 'Empty'
        else: 
            ret_text = '\n'.join(text)
            print timestamp, db_timestamp, ret_text
            return ret_text

class set_msg:
    def GET(self):
        d = web.input()
        msg = d.msg
        user = d.user

        fo = open(com_fn, 'a')
        fo.write('%f,%s,%s\n' % (time(), user, msg))
        fo.close()
        
        log  = 'Msg: ' + msg + ' received from ' + user + '\n'
        return log

app = web.application(urls, globals(), web.reloader) # There's web.profiler too

if __name__ == "__main__": 
    app.run()

# vim: set tabstop=4 shiftwidth=4 expandtab :
