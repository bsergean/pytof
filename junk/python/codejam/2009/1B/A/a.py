#!/usr/bin/env python
# vim: set tabstop=4 shiftwidth=4 expandtab
from __future__ import with_statement

from contextlib import nested
from os.path import expanduser, join
import os
import re
from pdb import set_trace
from time import clock
from shutil import copy

in_fn = 'in'
out_fn = 'out'

this_file = join(os.getcwd(), __file__)
desktop = join(expanduser('~'), 'Desktop')
copy(this_file, desktop)

def process(input):
    with open('only_tree') as f:

        text = f.read()
        print text

        p = re.compile('([a-z]+)')
        def tree_repl(match):
            return ",'%s'," % (match.groups()[0])
        text = p.sub(tree_repl, text)
        text = text.replace(')', '),')

        print text
        tree = eval(text)
        print type(tree)

        sys.exit(0)

    lines = input.splitlines()
    N = int(lines[0])

    samples = lines[1:N+1]
    print samples

    def compute_test_case(sample):
        return res 

    start = clock()
    cnt = compute_test_case_rec(samples[1], 'welcome to code jam')
    print "Time taken (seconds) = %.6f" % (clock()-start)
    
    print 
    print 2 * 'xxxxxxx\n' + 'cnt:', cnt
    print 2 * 'xxxxxxx\n'
    # return ''

    out = []
    for i, sample in enumerate(samples): 
        print i
        case = 'Case #%d: %s' % (i+1, compute_test_case(sample))
        out.append(case)

    res =  os.linesep.join(out) + os.linesep
    print res
    return res

    # test
    if True:
        with open(out_fn) as f:
            return f.read()

if __name__ == "__main__":

    if True:
        with open(in_fn) as f:
            input = f.read()
            output = process(input)

            out_fn = join(expanduser('~'), 'Desktop', 'out.txt')
            with open(out_fn, 'w') as fo:
                fo.write(output)

    import sys
    sys.exit(0)
    
    test = True
    if test:
        with nested(open(in_fn), open(out_fn)) as (f_in, f_out):
        
            input = f_in.read()
            output = f_out.read()
            assert process(input) == output
            print 'Youpi'
