#!/usr/bin/env python
# vim: set tabstop=4 shiftwidth=4 expandtab
from __future__ import with_statement

from contextlib import nested
from os.path import expanduser, join
import os
from pdb import set_trace
from time import clock
from shutil import copy

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
    print samples

    def permutations(L):
        if len(L) <= 1:
            yield L
        else:
            a = [L.pop(0)]
            for p in permutations(L):
                for i in range(len(p)+1):
                    yield p[:i] + a + p[i:]

    def permute_in_place(a, numb):
        a.sort()
        yield list(a)

        foo = list( [0] + str(numb) )
        print foo

        if len(a) <= 1:
            return

        first = 0
        last = len(a)
        while 1:
            i = last - 1

            while 1:
                i = i - 1
                if a[i] < a[i+1]:
                    j = last - 1
                    while not (a[i] < a[j]):
                        j = j - 1
                    a[i], a[j] = a[j], a[i] # swap the values
                    r = a[i+1:last]
                    r.reverse()
                    a[i+1:last] = r

                    # new_numb = int(''.join(map(str, a)))
                    new_numb = sum([v * 10 ** (len(a)-i-1) for i,v in enumerate(a)])
                    print new_numb, numb

                    if new_numb > numb:
                        yield list(a)
                        return
                    break

                if i == first:
                    a.reverse()
                    return
                        
    def compute_test_case(sample):
        L = [int(i) for i in sample] + [0]
        print L

        perms = {}

        new_p = 1
        for p in permute_in_place(L, int(sample)):
            # print p
            new_p = p

        new_numb = int(''.join(map(str, new_p)))
        return str(new_numb)

    start = clock()
    cnt = compute_test_case('511') # samples[1])
    # cnt = compute_test_case(samples[1])
    print "Time taken (seconds) = %.6f" % (clock()-start)
    # return cnt
    
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
