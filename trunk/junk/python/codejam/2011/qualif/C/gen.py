#!/usr/bin/env python

import random

T = 5
print T
Ci = 1000 * 1000
for i in xrange(T):
    N = 1000
    L = [random.randint(0, Ci) for i in xrange(N)]
    L = [str(i) for i in L]
    print N
    print ' '.join(L)
