# FreeBSD ls
# http://www.freebsd.org/cgi/cvsweb.cgi/src/bin/ls/print.c?rev=1.76.12.1;content-type=text%2Fplain

import os, sys

#
# There's this terminfo database I've never understood
# man tput gives more infos about that. I don't know 
# how to query that from python, except by using the curses module
#
terminal_cols  = int(os.popen('tput cols ').read())
terminal_lines = int(os.popen('tput lines').read())

path = sys.argv[1] if len(sys.argv) > 1 else '.'

entries  = os.listdir(path)
entries  = [e for e in entries if not e.startswith('.')] # get rid of config files
longuest = max(len(e) for e in entries) # will be the length of the longuest entry
cols = terminal_cols / longuest

items = []
lines = len(entries) / cols
for l in xrange(lines):
    s = ''
    for col in xrange(cols):
        idx = l + col * lines
        if idx < len(entries):
            s += entries[idx].ljust(longuest)
    print s
