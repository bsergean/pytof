#!/usr/bin/env python

class Robot:
    def __init__(self, N, P):
        self.N = N
        self.P = P

    def compute(self, n, p):

        if n <= 1 and p <= 1: return 1
    
        for j in xrange(P):
            res += Robot(n-1,j)

        return res

r = Robot(7,3)
print r.compute()
