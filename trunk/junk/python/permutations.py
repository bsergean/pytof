#!/usr/bin/env python

def gen(V, k):
    if k <= 1: 
        return V
    else:
        res = []
        for u in V:
            for v in gen(V, k-1):
                res.append(u+v)
        return res

print gen(['A', 'C', 'G', 'T'], 3)
