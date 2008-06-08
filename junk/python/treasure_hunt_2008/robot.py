#!/usr/bin/env python

cache = {}
def set_cache_result(n, p, res):
    key = '%d,%d' % (n, p)
    cache[key] = res

def is_in_cache(n, p):
    key = '%d,%d' % (n, p)
    return key in cache

def get_cache_result(n, p):
    key = '%d,%d' % (n, p)
    return cache[key]

def robot(n, p):

    if n == 1 or p == 1: return 1

    if is_in_cache(n,p):
        return get_cache_result(n,p)

    res = 0
    for j in xrange(1, p+1):
        res += robot(n-1, j)

    return res

def populate_cache(n, p):
    
    for i in xrange(1, n+1):
        for j in xrange(1, p+1):
            res = robot(i,j)
            print i,j,res
            set_cache_result(i,j,res)

import sys
if len(sys.argv) == 3:
    n, p = sys.argv[1:]
    print populate_cache(int(n), int(p))
else:
    print populate_cache(47, 43)
