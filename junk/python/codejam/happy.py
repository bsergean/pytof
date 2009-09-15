#!/usr/bin/env python
# vim: set tabstop=4 shiftwidth=4 expandtab
from __future__ import with_statement

from contextlib import nested
from os.path import expanduser, join
import os
from pdb import set_trace
from time import clock
from shutil import copy
from pdb import set_trace

in_fn = 'in'
out_fn = 'out'

this_file = join(os.getcwd(), __file__)
desktop = join(expanduser('~'), 'Desktop')
copy(this_file, desktop)

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
    samples = [ [int(i) for i in s.split()] for s in samples]
    print samples

    import string
    dd = dict(zip(range(10), list(string.digits)))

    @memoize
    def convDecToBase(num, base):
        # if not 2 <= base <= 10:
        #    raise ValueError, 'The base number must be between 2 and 36.'
        if num == 0: return ''
        num, rem = divmod(num, base)
        return convDecToBase(num, base)+dd[rem]

    cycles = {}
    import sys
    happy_dict = {}
    def happy(n, b): # orig

        n_as_numb = int( n, b )
        # print n, b, orig, 'numb', n_as_numb

        if (n_as_numb,b) in happy_dict:
            return happy_dict[ n_as_numb,b ]

        if n_as_numb in cycles:
            # print 'found in cycle'
            if n_as_numb < 1000:
                happy_dict[ n_as_numb,b ] = False
            return False
        cycles[n_as_numb] = True

        if n_as_numb == 1: 
            if n_as_numb < 1000:
                happy_dict[ n_as_numb,b ] = True
            return True
        else:
            S = sum( int(i)**2 for i in n )
            # print 'S1', S
            # Write S in base b
            S = convDecToBase(S, b)
            # print 'S2', S

            return happy(S, b) #, orig

    def compute_happy(L):
        i = min(L)
        while True:
            found = True
            for j in L:
                # print i,j,L
                cycles.clear()
                if not happy( convDecToBase(i,j), j):
                    found = False
                    break

            # if i >= 90: set_trace()
            if found: return i
            else: i += 1

    if False:
        start = clock()
        print convDecToBase(8, 2)
        h = happy('31', 10, 31) # samples[1])
        cycles.clear()
        print h
        h = happy('10', 2, 2) # samples[1])
        cycles.clear()
        print h
        h = happy(convDecToBase(5,3), 3, 5) # samples[1])
        cycles.clear()
        print h
        n = convDecToBase(91, 9)
        h = happy(n, 9, 91) # samples[1])
        cycles.clear()
        print h
        n = convDecToBase(91, 10)
        h = happy(n, 10, 91) # samples[1])
        cycles.clear()
        print h
        print "Time taken (seconds) = %.6f" % (clock()-start)
        # return cnt
    
    out = []
    for i, sample in enumerate(samples): 
        print 'Case', i+1
        case = 'Case #%d: %s' % (i+1, compute_happy(sample))
        # print case
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
