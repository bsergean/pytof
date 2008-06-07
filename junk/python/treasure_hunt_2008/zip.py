#!/usr/bin/env python

''' find GooSDFSDFSD -type f | xargs cat
Only int in files
'''

import os
from os.path import join

path = 'GoogleTreasureHunt08_5509866666541050969'
os.chdir(path)

def walker(path, pattern, ext):
    for d in os.walk('.'):
        for f in d[2]:
            fp = join(d[0], f)
            if fp.endswith(ext) and pattern in fp:
                yield fp

def lines_as_int(files, line_number):
    for f in files:
        lines = open(f).read().splitlines()
        for i, l in enumerate(lines):
            if i+1 == line_number:
                yield int(l)

js_files = walker('.', 'mno', '.rtf')
S1 = sum(lines_as_int(js_files, 4))
print S1

js_files = walker('.', 'abc', '.pdf')
S2 = sum(lines_as_int(js_files, 2))

print S1 * S2

# for p in pdf_files: print p
