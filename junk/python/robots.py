#!/usr/bin/env python

# from http://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
class memoized(object):
   """Decorator that caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned, and
   not re-evaluated.
   """
   def __init__(self, func):
      self.func = func
      self.cache = {}
   def __call__(self, *args):
      try:
         return self.cache[args]
      except KeyError:
         self.cache[args] = value = self.func(*args)
         return value
      except TypeError:
         # uncachable -- for instance, passing a list as an argument.
         # Better to not cache than to blow up entirely.
         return self.func(*args)

@memoized
def fact(n):
    if n <= 1: return 1
    return n * fact(n-1)

def closed_form(N, M):
    '''
    # (N+M-2)!/(N-1)!/(M-1)!

    (explanation from http://tinyurl.com/yj4n9ar)
    To get from the top corner to the bottom corner, we have to go down M-1 times
    and go to the right N-1 times.  We can consider each path as a string of Rs and
    Ds, where R means move right and D means move down. We know our string will
    have M-1 Ds and N-1 Rs in any order. Consider how many letters that is: M-1 +
    N-1 = M+N-2 How many ways are there to arrange this many letters? Well assume
    all the letters are unique; then the answer is just (M+N-2)!  But.. we have to
    realize that since we dont have unique objects the answer is actually gonna be
    smaller.  We can solve this easily by considering a 4x4 matrix and then scaling
    up.  For a 3x3 matrix we could have for example: RDRD ^ ^ that R and the other
    R could have been switched but are still the same path Now we can just consider
    how many ways the Rs could have been arranged. 2! or if we scale it up... N-1!
    This number is simply the number of duplicates for each and EVERY path we have.
    How about the Ds.. same thing M-1!  Now we divide our original result that
    assumed each path was unique by the number of duplicates per path.  This is
    simply (N+M-2)!/(N-1)!/(M-1)!
    '''
    return fact(N+M-2) / fact(N-1) / fact(M-1)

@memoized
def rec(n,p):
    if n <= 1 or p <= 1: return 1
    return rec(n-1,p) + rec(n,p-1)

import sys
print rec( int(sys.argv[1]), int(sys.argv[2]) )

if False:
    N, P = 100, 100
    for i in xrange(1, N):
        for j in xrange(1, P):
            print 'DP', i, j, rec(i,j)
            assert rec(i,j) == closed_form(i,j)
