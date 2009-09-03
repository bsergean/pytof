#!/usr/bin/env python
# vim: set tabstop=4 shiftwidth=4 expandtab
from __future__ import with_statement

from contextlib import nested
import os

# L letters
# D words

in_fn = 'input-sample.in'
out_fn = 'output-sample'

def process(input):
    lines = input.splitlines()
    L, D, N = map(int, lines[0].split())

    print 'params', L, D, N
    words = lines[1:D]
    print 'words', words
    test_cases = lines[D+1:D+1+N]
    print 'test_cases', test_cases

    def compute_test_case(words, tc):
        # (2, 1, 3, 0):
        return 2

    out = ( 'Case %d: %d' % (i, compute_test_case(words, tc)) \
            for i,tc in enumerate(test_cases) )

    res =  os.linesep.join(out)
    print res
    return res

    # test
    if True:
        with open(out_fn) as f:
            return f.read()

if __name__ == "__main__":

    test = True
    if test:
        with nested(open(in_fn), open(out_fn)) as (f_in, f_out):
        
            input = f_in.read()
            output = f_out.read()
            assert process(input) == output
            print 'Youpi'
