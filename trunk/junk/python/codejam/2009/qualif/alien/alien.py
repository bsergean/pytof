#!/usr/bin/env python
# vim: set tabstop=4 shiftwidth=4 expandtab
from __future__ import with_statement

from contextlib import nested
import os
import re

# L letters
# D words

in_fn = 'input-sample.in'
out_fn = 'output-sample'
p = re.compile('(\(\w*\)|\w{1})')

def process(input):
    lines = input.splitlines()
    L, D, N = map(int, lines[0].split())

    # L is not used thanks to splitlines that chomp the line
    print 'params', L, D, N
    words = lines[1:D+1]
    print 'words', words
    test_cases = lines[D+1:D+1+N]
    print 'test_cases', test_cases

    def compute_test_case(words, tc, L):
        # (2, 1, 3, 0):
        tokens = p.findall(tc)
        # print tokens

        S = 0
        for word in words:
            T = 0
            # print word
            for letter, token in zip(word, tokens):
                if letter in token:
                    T += 1

            if T == L:
                S += 1
                # print '-> yep'

        return S

    out = ( 'Case #%d: %d' % (i+1, compute_test_case(words, tc, L)) \
            for i,tc in enumerate(test_cases) )

    res =  os.linesep.join(out) + os.linesep
    # print res
    return res

    # test
    if True:
        with open(out_fn) as f:
            return f.read()

if __name__ == "__main__":

    with open(in_fn) as f:
        input = f.read()

        output = process(input)

        with open('/tmp/res.txt', 'w') as fo:
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
