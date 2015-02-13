#!/usr/bin/env python
''' ./C.py < sample.in | tee out && diff out sample.out
'''

import sys
import pdb

from collections import deque

def addBin(a, b):
    aBin = bin(a)[2:]
    bBin = bin(b)[2:]

    lA = len(aBin)
    lB = len(bBin)

    if lA > lB:
        bBin = bBin.zfill(lA)
    elif lB > lA:
        aBin = aBin.zfill(lB)

    assert len(aBin) == len(bBin)

    res = len(aBin) * ['']
    k = 0
    for i, j in zip(aBin, bBin):
        if i == '0' and j == '0':
            out = '0'
        elif i == '0' and j == '1':
            out = '1'
        elif i == '1' and j == '0':
            out = '1'
        elif i == '1' and j == '1':
            out = '0'
        else:
            print 'Error'

        res[k] = out
        k += 1

    binResult = ''.join(res)
    return s2b(binResult)

def s2b(s):
    # s = s[::-1]
    L = len(s) 

    ret = 0
    for i in xrange(L):
        if s[i] == '1':
            # ret += 1 << i # if you reverse s
            ret += 1 << (L - i - 1)

    return ret

b = bin(12335)
assert s2b(b) == 12335
assert s2b('11000000101111') == 12335

#print s2b('1100')
#print s2b('0101')

# pdb.set_trace()
addBin(12, 5)

assert 1 == addBin(4, 5)
assert 14 == addBin(9, 7)
assert 56 == addBin(10, 50)

def compute(candies):

    candies = deque(candies)

    L = len(candies)
    winner = -1
    for i in xrange(L):
        for i in xrange(0, L-1):
            A = 0
            realA = 0
            B = 0
            realB = 0
            j = 0
            while j <= i:
                A = addBin(A, candies[j])
                realA += candies[j]
                j += 1

            k = L - 1
            while k > i:
                B = addBin(B, candies[k])
                realB += candies[k]
                k -= 1

            if A == B:
                candidate = max(realA, realB)
                if candidate > winner:
                    winner = candidate
                
        candies.rotate()

    if winner == -1: return 'NO'
    else: return winner

ret = compute(range(5))
assert ret == 'NO'
ret = compute([3, 5, 6])
assert ret == 11

if __name__ == '__main__':
    answers = [
        'NO', 11
    ]
    answers = []

    T = sys.stdin.readline()
    T = int(T)
    for j in xrange(T):
        N = sys.stdin.readline()
        N = int(N)
        candies = sys.stdin.readline()
        candies = [int(i) for i in candies.split()]
        assert len(candies) == N
        answer = compute(candies)
        output = 'Case #%d: %s\n' % (j+1, answer)
        sys.stdout.write(output)
        sys.stderr.write(output)
        

    
