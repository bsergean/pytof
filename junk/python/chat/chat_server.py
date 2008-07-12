#!/usr/bin/env python

'''
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

messages = []

class up:
    def GET(self):
        return ''

class all:
    def GET(self):

        d = web.input()
        user      = d.user
        index     = int(d.index)

        text = []
        for tokens in messages[index:]:

            db_user      = tokens[0]
            msg          = urlsafe_b64decode(tokens[1])

            if db_user != user:
                text.append(db_user + '> ' + msg)

        if not len(text): return 'Empty'
        else: 
            text.insert(0, str(len(messages)))
            ret_text = '\n'.join(text)
            return ret_text

class set_msg:
    def GET(self):
        d = web.input()
        msg = d.msg
        user = d.user

        messages.append([user, msg])
        return ''

app = web.application(urls, globals(), web.reloader) # There's web.profiler too

if __name__ == "__main__": 
    app.run()

# vim: set tabstop=4 shiftwidth=4 expandtab :
