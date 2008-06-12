#!/usr/bin/env python

cache = []
def set_cache_result(n, p, res):
    cache[n][p] = res

def is_in_cache(n, p):
    return cache[n][p] != -1

def get_cache_result(n, p):
    return cache[n][p]

def robot(n, p):

    if n == 1 or p == 1: return 1

    if is_in_cache(n,p):
        return get_cache_result(n,p)

    res = 0
    for j in xrange(1, p+1):
        res += robot(n-1, j)

    return res

def populate_cache(n, p):

    # init
    for i in xrange(0, n+1):
        L = [-1 for j in xrange(0, p+1)]
        cache.append(L)
    
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
