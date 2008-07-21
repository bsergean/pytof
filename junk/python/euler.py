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

level25()
