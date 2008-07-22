#!/usr/bin/env python

import sys
from math import fmod

def infinite():
    i = 0
    while True:
        yield i
        i += 1

def multiple_fmod(x, Max):
    return [i for i in xrange(x, Max) if fmod(i, x) == 0]

def level1():

    Max = 1000
    # Max = 10
    m3 = set(multiple_fmod(3, Max))
    m5  = set(multiple_fmod(5, Max))

    U = m3.union(m5)
    print sum(U)

def level2():

    fibo_cache = {}
    def fibo(i):
        if i in fibo_cache:
            return fibo_cache[i]

        if i <= 1:
            return 1
        return fibo(i-1) + fibo(i-2)

    for i in xrange(1,10): print fibo(i)

    S = 0
    i = 1
    while True:
        f = fibo(i)
        fibo_cache[i] = f
        i += 1
        if f % 2: continue
        if f >= 4e6:
            print S
            break
        S += f

# Level 3
# http://fr.wikipedia.org/wiki/D%C3%A9composition_en_produit_de_facteurs_premiers

# http://www.daniweb.com/code/snippet305.html
# fast prime number list generator using a sieve algorithm

def gen_primes(n):
  """ returns a list of prime numbers from 2 to < n """
  if n < 2:  return []
  if n == 2: return [2]
  # do only odd numbers starting at 3
  s = range(3, n, 2)
  # n**0.5 may be slightly faster than math.sqrt(n)
  mroot = n ** 0.5
  half = len(s)
  i = 0
  m = 3
  while m <= mroot:
    if s[i]:
      j = (m * m - 3)//2
      s[j] = 0
      while j < half:
        s[j] = 0
        j += m
    i = i + 1
    m = 2 * i + 3
  # make exception for 2
  return [2]+[x for x in s if x]

def compute_primes_native(max_int):
    primes = {}
    for p in gen_primes(max_int):
        primes[p] = None
    return primes

N = 600851475143.0
max_int = int((N ** 0.5) + 1)
primes = compute_primes_native(max_int)

def is_prime(i, primes):
  # do only odd numbers starting at 3
  s = range(3, n, 2)

def level3():

    i = 2.0
    while i < N:
        if fmod(N,i) == 0:
            print i
            print N / i
            if i in primes and N / i in primes:
                print i, 'is a prime ->', N / i
            print
        i += 1

        #sys.stdout.write('\r%f' % i)

#level3()


def get_pythagorean(sum):
    for a in xrange(1, sum):
        for b in xrange(a, sum):
            for c in xrange(b, sum):
                if (a+b+c == sum and a*a+b*b==c*c):
                    return a,b,c,a*b*c
    return "no results found"

def level9():
    print get_pythagorean(1000)

#level9()


def is_palindrome_str(num):
    liste = list(str(num))
    liste2 = list(str(num))
    liste.reverse()
    if (liste == liste2):
        return True
    return False

from math import log10
def is_palindrome_num(num):
    liste = [int(s) for s in str(num)]
    i = 0
    j = len(liste) - 1
    while i < j:
        if liste[i] != liste[j]:
            return False
        i += 1
        j -= 1
    return True

def is_palindrome(num):
    return is_palindrome_num(num)

def find_palindromic():
    results = {} 
    for a in xrange(100,1000):
        for b in xrange(100,1000):
            p = a*b
            if(is_palindrome(p) and a != b):
                results[p] = (a,b)

    return max(results.keys())

def level4():
    print find_palindromic()

def level5():
    X = 20
    divisors = range(1,21)
    divisors.reverse()
    while True:
        if all((fmod(X,i) == 0.0 for i in divisors)):
            print X
            return
        X += 20

def level6():
    def diff(X):
        S_square = [i * i for i in xrange(1,X+1)]
        a = sum(S_square)
        S_linear_square = [i for i in xrange(1,X+1)]
        b = sum(S_linear_square) ** 2
        print b - a
    diff(10)
    diff(100)

def level7():
    max_int = 10000
    primes = compute_primes_native(max_int)
    while len(primes) < 10005:
        max_int += 1000
        primes = compute_primes_native(max_int)
    
    print sorted(primes.keys())[10000]

def level8():
    a = '7316717653133062491922511967442657474235534919493496983520312774506326239578318016984801869478851843858615607891129494954595017379583319528532088055111254069874715852386305071569329096329522744304355766896648950445244523161731856403098711121722383113622298934233803081353362766142828064444866452387493035890729629049156044077239071381051585930796086670172427121883998797908792274921901699720888093776657273330010533678812202354218097512545405947522435258490771167055601360483958644670632441572215539753697817977846174064955149290862569321978468622482839722413756570560574902614079729686524145351004748216637048440319989000889524345065854122758866688116427171479924442928230863465674813919123162824586178664583591245665294765456828489128831426076900422421902267105562632111110937054421750694165896040807198403850962455444362981230987879927244284909188845801561660979191338754992005240636899125607176060588611646710940507754100225698315520005593572972571636269561882670428252483600823257530420752963450'
    print a
    liste = [int(s) for s in str(a)]
    i = 0
    M = -1
    for i in xrange(0,len(a) - 5):
        L = liste[i:i+5]
        x = reduce(lambda x,y: x*y, L)
        print x, L
        if x > M:
            M = x
    print M
    # pipe to sort -n to have a nice output

def level10():
    max_int = 2e6
    primes = compute_primes_native(max_int)
    print sum(primes.keys())

mat_str='''08 02 22 97 38 15 00 40 00 75 04 05 07 78 52 12 50 77 91 08
49 49 99 40 17 81 18 57 60 87 17 40 98 43 69 48 04 56 62 00
81 49 31 73 55 79 14 29 93 71 40 67 53 88 30 03 49 13 36 65
52 70 95 23 04 60 11 42 69 24 68 56 01 32 56 71 37 02 36 91
22 31 16 71 51 67 63 89 41 92 36 54 22 40 40 28 66 33 13 80
24 47 32 60 99 03 45 02 44 75 33 53 78 36 84 20 35 17 12 50
32 98 81 28 64 23 67 10 26 38 40 67 59 54 70 66 18 38 64 70
67 26 20 68 02 62 12 20 95 63 94 39 63 08 40 91 66 49 94 21
24 55 58 05 66 73 99 26 97 17 78 78 96 83 14 88 34 89 63 72
21 36 23 09 75 00 76 44 20 45 35 14 00 61 33 97 34 31 33 95
78 17 53 28 22 75 31 67 15 94 03 80 04 62 16 14 09 53 56 92
16 39 05 42 96 35 31 47 55 58 88 24 00 17 54 24 36 29 85 57
86 56 00 48 35 71 89 07 05 44 44 37 44 60 21 58 51 54 17 58
19 80 81 68 05 94 47 69 28 73 92 13 86 52 17 77 04 89 55 40
04 52 08 83 97 35 99 16 07 97 57 32 16 26 26 79 33 27 98 66
88 36 68 87 57 62 20 72 03 46 33 67 46 55 12 32 63 93 53 69
04 42 16 73 38 25 39 11 24 94 72 18 08 46 29 32 40 62 76 36
20 69 36 41 72 30 23 88 34 62 99 69 82 67 59 85 74 04 36 16
20 73 35 29 78 31 90 01 74 31 49 71 48 86 81 16 23 57 05 54
01 70 54 71 83 51 54 69 16 92 33 48 61 43 52 01 89 19 67 48
'''

def read_input(var):
    lines = [l for l in var.splitlines()]
    mat = [map(int, l.split()) for l in lines]
    return mat

class Matrix:
    def __init__(self, m):
        from copy import deepcopy
        self.m = deepcopy(m)

        self.N = len(m[0])
        self.M = len(m)

    def col(self, i):
        return [self.m[k][i] for k in range(self.M)]
    
    def cols(self):
        return [self.col(i) for i in range(self.N)]

    def row(self, i):
        return [self.m[i][k] for k in range(self.N)]

    def rows(self):
        return [self.row(i) for i in range(self.M)]

    def diag_ne(self): # north east
        diags = []

        for k in xrange(0, self.M):
            i,j = self.N - 1, k
            res = []
            while i >= 0 and j < self.M:
                res.append(self.m[i][j])
                i -= 1
                j += 1
            print res
            if len(res) >= 4:
                diags.append(res)

        for k in xrange(0, self.N):
            i,j = k, 0
            res = []
            while i >= 0 and j < self.M:
                res.append(self.m[i][j])
                i -= 1
                j += 1
            print res
            if len(res) >= 4:
                diags.append(res)
        self.max_func(diags)

    def diag_se(self): # south east
        diags = []
        for k in xrange(0, self.N):
            i,j = k,0
            res = []
            while i < self.N and j < self.M:
                res.append(self.m[i][j])
                i += 1
                j += 1
            print res
            if len(res) >= 4:
                diags.append(res)
        for l in xrange(0, self.M):
            i,j = 0,l
            res = []
            while i < self.N and j < self.M:
                res.append(self.m[i][j])
                i += 1
                j += 1
            print res
            if len(res) >= 4:
                diags.append(res)

        self.max_func(diags)

    def max_func(self, _list, verbose = False):
        x = -1
        for c in _list:
            for i in range(0, len(c) - 3):
                L = c[i:i+4]
		r = reduce(lambda x,y: x*y, L)
		if verbose: print L, r
		if r > x: x = r
            if verbose: print
        print x
	return x

    def max_cols(self):
        self.max_func(self.cols())

    def max_rows(self):
        self.max_func(self.rows())
                
def level11():
    mat = read_input(mat_str)
    A = Matrix(mat)
    A.max_cols()
    A.max_rows()
    A.diag_se()
    A.diag_ne()

def level12():
    def triangle_numbers():
        S = 1
        i = 1
        while True:
            yield S
            i += 1
            S += i

    def factors(n):
        F = [1]
        for i in xrange(2,n+1):
            if fmod(n, i) == 0:
                F.append(i)
        return F

    def nb_factors(n):
        return len(factors(n))

    if False: # Brute force takes forever
        i = 1
        for n in triangle_numbers():
            N = nb_factors(n)
            if N > 100:
                print i, N
            if N > 500:
                break
            i += 1

def level25():

    fibo_cache = {}
    def fibo(i):
        if i in fibo_cache:
            return fibo_cache[i]

        if i <= 1:
            return 1
        return fibo(i-1) + fibo(i-2)

    for i in xrange(1,10): print fibo(i)

    S = 0
    i = 1
    while True:
        f = fibo(i)
        fibo_cache[i] = f
        i += 1
        f_str = str(f)
        if len(f_str) >= 1000:
            print i
            break

level12()
