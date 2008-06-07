#!/usr/bin/env python

'''
http://www.cs.arizona.edu/icon/oddsends/primes.htm

Find the smallest number that can be expressed as
the sum of 5 consecutive prime numbers,
the sum of 11 consecutive prime numbers,
the sum of 775 consecutive prime numbers,
the sum of 1151 consecutive prime numbers,
and is itself a prime number.

For example, 41 is the smallest prime number that can be expressed as
the sum of 3 consecutive primes (11 + 13 + 17 = 41) and
the sum of 6 consecutive primes (2 + 3 + 5 + 7 + 11 + 13 = 41). 

Result: 8429539
Time: 3 minutes
'''

def compute_primes_from_arizona():
    primes = {}
    for l in open('primes_from_arizona.txt').read().splitlines():
        for p in l.split():
            primes[int(p)] = None 
    return primes

import sys
# No results for big number under 1M 
max_int = int(sys.argv[1])
def compute_primes_native():
    from prime_generator import gen_primes
    primes = {}
    for p in gen_primes(max_int):
        primes[p] = None
    return primes

primes = compute_primes_from_arizona()
primes = compute_primes_native()
sorted_primes = sorted(primes.keys()) 

def walk_and_sum(tget):
    candidates = []

    N = len(sorted_primes)
    for p in xrange(N):
        if p + tget >= N: break
        sum_primes = sorted_primes[p:p+tget]

        S = sum(sum_primes)
        if S in primes:
            candidates.append(S)

    return candidates

from sets import Set
main_set = Set(walk_and_sum(5))

for p in [11, 775, 1151]:
    new_list = walk_and_sum(p)
    print p, sorted(new_list)

    new_set = Set(new_list)
    main_set &= new_set

    print main_set

    

