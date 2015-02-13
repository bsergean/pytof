#!/usr/bin/env python
import random

samples = 10000
print samples
for i in xrange(samples):
    if True:
        N = random.randint(1, 10)
        K = random.randint(1, 100)
    else:
        N = random.randint(1, 30)
        K = random.randint(1, 10 ** 8)

    print N, K

