#!/usr/bin/env python

""" http://www.cs.arizona.edu/icon/oddsends/primes.htm """

def primes():
    for l in open('primes_from_arizona.txt').read().splitlines():
        for p in l.split():
            yield int(p)

for p in primes():
    print p

