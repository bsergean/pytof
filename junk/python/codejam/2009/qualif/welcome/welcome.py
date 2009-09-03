#!/usr/bin/env python
# vim: set tabstop=4 shiftwidth=4 expandtab
from __future__ import with_statement

from contextlib import nested
from os.path import expanduser, join
import os
from pdb import set_trace
from time import clock

in_fn = 'in'
out_fn = 'out'

# http://code.activestate.com/recipes/466320/
from cPickle import dumps, PicklingError # for memoize
class memoize(object):
    """Decorator that caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned, and
    not re-evaluated. Slow for mutable types."""
    # Ideas from MemoizeMutable class of Recipe 52201 by Paul Moore and
    # from memoized decorator of http://wiki.python.org/moin/PythonDecoratorLibrary
    # For a version with timeout see Recipe 325905
    # For a self cleaning version see Recipe 440678
    # Weak references (a dict with weak values) can be used, like this:
    #   self._cache = weakref.WeakValueDictionary()
    #   but the keys of such dict can't be int
    def __init__(self, func):
        self.func = func
        self._cache = {}
    def __call__(self, *args, **kwds):
        key = args
        if kwds:
            items = kwds.items()
            items.sort()
            key = key + tuple(items)
        try:
            if key in self._cache:
                return self._cache[key]
            self._cache[key] = result = self.func(*args, **kwds)
            return result
        except TypeError:
            try:
                dump = dumps(key)
            except PicklingError:
                return self.func(*args, **kwds)
            else:
                if dump in self._cache:
                    return self._cache[dump]
                self._cache[dump] = result = self.func(*args, **kwds)
                return result

def process(input):
    lines = input.splitlines()
    N = int(lines[0])

    samples = lines[1:N+1]
    print samples

    # @memoize
    def compute_test_case_rec(sample, welcome):
        # print 'sample:', sample
        # print 'welcome:', welcome

        # find the first letter of welcome in sample
        if welcome != '':
            f = welcome[0]

            # print 'searching', f

            S = 0
            start = 0
            i = 0
            while i != -1:
                i = sample.find(f, start)
                # print 'find ->', i

                if i != -1: # found
                    
                    # we reached the last char:
                    S += compute_test_case_rec(sample[i+1:], welcome[1:])
                    start = i + 1

            return S

        else:
            # print '-> welcome found'
            return 1


    def compute_test_case(sample):

        cnt = compute_test_case_rec(sample, 'welcome to code jam')
        # cnt = 1
        res = str(cnt % 10000).zfill(4)
        return res 

    start = clock()
    cnt = compute_test_case_rec(samples[1], 'welcome to code jam')
    print "Time taken (seconds) = %.6f" % (clock()-start)
    
    print 
    print 2 * 'xxxxxxx\n' + 'cnt:', cnt
    print 2 * 'xxxxxxx\n'
    # return ''

    out = ( 'Case #%d: %s' % (i+1, compute_test_case(sample)) \
            for i, sample in enumerate(samples) )

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

    import sys
    # sys.exit(0)
    
    test = True
    if test:
        with nested(open(in_fn), open(out_fn)) as (f_in, f_out):
        
            input = f_in.read()
            output = f_out.read()
            assert process(input) == output
            print 'Youpi'
