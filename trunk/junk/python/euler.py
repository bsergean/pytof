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

level8()
