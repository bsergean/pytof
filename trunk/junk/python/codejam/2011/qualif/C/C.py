#!/usr/bin/env python
''' 
./C.py < sample.in | tee out && diff out sample.out
./C_slow_correct.py < input_real > out && diff -q out output_real_ok && echo OK
'''

import sys
import pdb

from collections import deque

B0  = 1 << 0;
B1  = 1 << 1;
B2  = 1 << 2;
B3  = 1 << 3;
B4  = 1 << 4;
B5  = 1 << 5;
B6  = 1 << 6;
B7  = 1 << 7;
B8  = 1 << 8;
B9  = 1 << 9;
B10 = 1 << 10;
B11 = 1 << 11;
B12 = 1 << 12;
B13 = 1 << 13;
B14 = 1 << 14;
B15 = 1 << 15;
B16 = 1 << 16;
B17 = 1 << 17;
B18 = 1 << 18;
B19 = 1 << 19;
B20 = 1 << 20;
B21 = 1 << 21;
B22 = 1 << 22;
B23 = 1 << 23;
B24 = 1 << 24;
B25 = 1 << 25;
B26 = 1 << 26;
B27 = 1 << 27;
B28 = 1 << 28;
B29 = 1 << 29;
B30 = 1 << 30;
B31 = 1 << 31;

def addBin(a, b):
    out = 0

    if ( (a & B0) != (b & B0) ): out += B0;
    if ( (a & B1) != (b & B1) ): out += B1;
    if ( (a & B2) != (b & B2) ): out += B2;
    if ( (a & B3) != (b & B3) ): out += B3;
    if ( (a & B4) != (b & B4) ): out += B4;
    if ( (a & B5) != (b & B5) ): out += B5;
    if ( (a & B6) != (b & B6) ): out += B6;
    if ( (a & B7) != (b & B7) ): out += B7;
    if ( (a & B8) != (b & B8) ): out += B8;
    if ( (a & B9) != (b & B9) ): out += B9;
    if ( (a & B10) != (b & B10) ): out += B10;
    if ( (a & B11) != (b & B11) ): out += B11;
    if ( (a & B12) != (b & B12) ): out += B12;
    if ( (a & B13) != (b & B13) ): out += B13;
    if ( (a & B14) != (b & B14) ): out += B14;
    if ( (a & B15) != (b & B15) ): out += B15;
    if ( (a & B16) != (b & B16) ): out += B16;
    if ( (a & B17) != (b & B17) ): out += B17;
    if ( (a & B18) != (b & B18) ): out += B18;
    if ( (a & B19) != (b & B19) ): out += B19;
    if ( (a & B20) != (b & B20) ): out += B20;
    if ( (a & B21) != (b & B21) ): out += B21;
    if ( (a & B22) != (b & B22) ): out += B22;
    if ( (a & B23) != (b & B23) ): out += B23;
    if ( (a & B24) != (b & B24) ): out += B24;
    if ( (a & B25) != (b & B25) ): out += B25;
    if ( (a & B26) != (b & B26) ): out += B26;
    if ( (a & B27) != (b & B27) ): out += B27;
    if ( (a & B28) != (b & B28) ): out += B28;
    if ( (a & B29) != (b & B29) ): out += B29;
    if ( (a & B30) != (b & B30) ): out += B30;
    if ( (a & B31) != (b & B31) ): out += B31;
    
    return out

addBinFast = addBin
assert 9 == addBinFast(12, 5)
assert 1 == addBinFast(4, 5)
assert 14 == addBinFast(9, 7)
assert 56 == addBinFast(10, 50)

def addBinSlow(a, b):
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

# addBin = addBinSlow

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

'''
./C.py < input_real > out && diff -q out output_real_ok && echo OK
'''

def compute(candies):
    candies = deque(candies)

    L = len(candies)
    winner = -1
    for z in xrange(L):
        for i in xrange(0, L-1):
            A = 0
            realA = 0
            B = 0
            realB = 0
            j = 0
            for elem in candies:
                if j <= i:
                    A ^= elem
                    realA += elem
                    j += 1
                else:
                    B ^= elem
                    realB += elem

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
        

    
