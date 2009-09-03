#!/usr/bin/env python
# vim: set tabstop=4 shiftwidth=4 expandtab
from __future__ import with_statement

from contextlib import nested
from os.path import expanduser, join
import os
import sys
from pdb import set_trace
from time import clock
from shutil import copy

in_fn = 'in'
out_fn = 'out'

this_file = join(os.getcwd(), __file__)
desktop = join(expanduser('~'), 'Desktop')
copy(this_file, desktop)

def process(input):
    lines = input.splitlines()
    T = int(lines[0])

    i = 1
    row = 1
    H, W = 1, 1
    maps = []

    while True:
        H, W = map(int, lines[row].split())
        # print H, W

        MapStr = lines[row+1:row+1+H]

        Map = []
        for r in MapStr:
            Map.append(r.split())
            
        maps.append(Map)

        i += 1
        row += H+1 
        if i > T: 
            break

    def compute_labels(Map):

        rows = []
        for row in Map:
            rows.append( ['a' for col in row] )

        return rows

    if False:
        start = clock()
        cnt = compute_test_case_rec(samples[1], 'welcome to code jam')
        print "Time taken (seconds) = %.6f" % (clock()-start)
        
        print 
        print 2 * 'xxxxxxx\n' + 'cnt:', cnt
        print 2 * 'xxxxxxx\n'
        # return ''

    out = []
    for i, Map in enumerate(maps): 
        case = 'Case #%d:' % (i+1) + os.linesep
        rows = []
        for row in compute_labels(Map):
            rows.append(' '.join(col for col in row))
        case += '\n'.join(rows)

        out.append(case)

    res =  os.linesep.join(out) + os.linesep
    print res
    return res

    # test
    if True:
        with open(out_fn) as f:
            return f.read()

if __name__ == "__main__":

    if False:
        with open(in_fn) as f:
            input = f.read()
            output = process(input)

            out_fn = join(expanduser('~'), 'Desktop', 'out.txt')
            with open(out_fn, 'w') as fo:
                fo.write(output)

    # sys.exit(0)
    
    test = True
    if test:
        with nested(open(in_fn), open(out_fn)) as (f_in, f_out):
        
            input = f_in.read()
            output = f_out.read()
            assert process(input) == output
            print 'Youpi'
