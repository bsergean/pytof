#!/usr/bin/env python

import sys
import calendar
import StringIO
import re
from math import fmod, log10
from time import clock
from copy import deepcopy
from decimal import *

try:
    import psyco
    psyco.full()
except ImportError:
    pass

# http://code.activestate.com/recipes/466320/
from cPickle import dumps, PicklingError # for memoize
class memoize(object):
    """Decorator that caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned, and
    not re-evaluated. Slow for mutable types."""
    # Ideas from MemoizeMutable class of Recipe 52201 by Paul Moore and
    # from memoized decorator of http://wiki.python.org/moin/PythonDecoratorLibrary
    # For a version with timeout see Recipe 325905
    # For a self cleaning version see Recipe 440678
    # Weak references (a dict with weak values) can be used, like this:
    #   self._cache = weakref.WeakValueDictionary()
    #   but the keys of such dict can't be int
    def __init__(self, func):
        self.func = func
        self._cache = {}
    def __call__(self, *args, **kwds):
        key = args
        if kwds:
            items = kwds.items()
            items.sort()
            key = key + tuple(items)
        try:
            if key in self._cache:
                return self._cache[key]
            self._cache[key] = result = self.func(*args, **kwds)
            return result
        except TypeError:
            try:
                dump = dumps(key)
            except PicklingError:
                return self.func(*args, **kwds)
            else:
                if dump in self._cache:
                    return self._cache[dump]
                self._cache[dump] = result = self.func(*args, **kwds)
                return result



def multiple_fmod(x, Max):
    return [i for i in xrange(x, Max) if fmod(i, x) == 0]

def list_of_int_to_int(L):
    ''' int(''.join(L)) will should be way faster ... '''
    return sum([v * 10 ** (len(L)-i-1) for i,v in enumerate(L)])

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
  # make exception for 2, we say that 1 is not a prime
  return [2] + [x for x in s if x]

def compute_primes_native(max_int):
    primes = {}
    for p in gen_primes(max_int):
        primes[p] = None
    return primes

def compute_sorted_primes(n):
    primes = compute_primes_native(n)
    primes = sorted(primes.keys())
    return primes

class Factoriser:
    def __init__(self, N):
        ''' http://www.btinternet.com/~se16/js/factor.htm '''
        max_int = int((N ** 0.5) + 1)
        primes = compute_primes_native(max_int)
        self.primes = sorted(primes.keys())

    def do_primal_factor(self, n):

        #max_int = int((n ** 0.5) + 1)
        max_int = n / 2 + 1

        factors = []
        for i in self.primes[:max_int]:
            if n % i == 0:
                factors.append(i)
        return factors

    def do_factorize_primal_factors(self, n):
        factors = self.do_primal_factor(n)
        print 'do_factorize_primal_factors', n, factors
        factors_power = [1 for f in factors]

        x = reduce(lambda x,y: x*y, factors)
        while x != n:
            try_mul = n / x
            print try_mul
            f_new = self.do_primal_factor(try_mul)
            print f_new 
            x_new = reduce(lambda x,y: x*y, f_new)

            x *= x_new
            for f in f_new:
                print 'fff', factors, f
                factors_power[factors.index(f)] += 1

        return [f ** power for f, power in zip(factors, factors_power)]

    def do_proper_divisors(self, n):
        max_int = n / 2 + 1

        factors = []
        for i in xrange(1,max_int):
            if n % i == 0:
                factors.append(i)
        return factors

    def proper_divisor_sum(self, n):
        return sum(self.do_proper_divisors(n))

def level3():
    N = 600851475143.0
    f = Factoriser(N)
    print f.do_primal_factor(N)

def get_pythagorean(sum):
    for a in xrange(1, sum):
        for b in xrange(a, sum):
            for c in xrange(b, sum):
                if (a+b+c == sum and a*a+b*b==c*c):
                    return a,b,c,a*b*c
    return "no results found"

def level9():
    print get_pythagorean(1000)

def is_palindrome_str(num):
    liste = list(str(num))
    liste2 = list(str(num))
    liste.reverse()
    if (liste == liste2):
        return True
    return False

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

def is_palindrome_builtin(num):
    ''' way faster ... slice magic ! '''
    s = str(num)
    return s == s[::-1]

def is_palindrome(num):
    return is_palindrome_builtin(num)

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
        if all((X % i == 0 for i in divisors)):
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
        '''
                M
           0 1 0 0 10 1
           0 1 0 0 10 1
        N  0 1 0 0 10 1
           0 1 0 0 10 1
           0 1 0 0 10 1
        '''
        self.m = deepcopy(m)

        self.N = len(m[0])
        self.M = len(m)

        self.i_cur = 0
        self.j_cur = self.M - 1
        self.value = 0

        self.i_center = self.N / 2
        self.j_center = self.M / 2

    def col(self, i):
        return [self.m[k][i] for k in range(self.M)]
    
    def cols(self):
        return [self.col(i) for i in range(self.N)]

    def row(self, i):
        return [self.m[i][k] for k in range(self.N)]

    def rows(self):
        return [self.row(i) for i in range(self.M)]

    def the_diag(self):
        return sum(self.m[i][i] for i in range(self.M))

    def the_other_diag(self):
        return sum(self.m[self.M - i - 1][i] for i in range(self.M))

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

    def set_decrement(self, i, j):
        self.m[i][j] = self.value
        self.value -= 1

    def set_increment(self):
        self.value += 1

    def center(self):
        return self.m[self.i_center][self.j_center]

    def fill_S(self):
        print 'fill_S'
        while True:
            i,j = self.i_cur, self.j_cur
            self.set_decrement(i,j)

            if i+1 == self.M or self.m[i+1][j] != 0:
                self.set_increment()
                break

            self.i_cur += 1

        print self.i_cur, self.j_cur

    def fill_N(self):
        print 'fill_N'
        while True:
            i,j = self.i_cur, self.j_cur
            self.set_decrement(i,j)

            if i == 0 or self.m[i-1][j] != 0:
                self.set_increment()
                break

            self.i_cur -= 1

        print self.i_cur, self.j_cur

    def fill_E(self):
        print 'fill_E'
        while True:
            i,j = self.i_cur, self.j_cur
            self.set_decrement(i,j)

            if j+1 == self.N or self.m[i][j+1] != 0:
                self.set_increment()
                break

            self.j_cur += 1

        print self.i_cur, self.j_cur

    def fill_W(self):
        print 'fill_W'
        while True:
            i,j = self.i_cur, self.j_cur
            self.set_decrement(i,j)

            if j == 0 or self.m[i][j-1] != 0:
                self.set_increment()
                break

            self.j_cur -= 1

        print self.i_cur, self.j_cur

    def filled(self):
        for c in self.cols():
            for i in c:
                if i == 0:
                    return False
        return True


    def __str__(self):
        fo = StringIO.StringIO()
        for r in self.rows():
            s = '[ ' + '\t'.join(map(str, r)) + ' ] ' + '\n'
            fo.write(s)
        return fo.getvalue()

def level11():
    mat = read_input(mat_str)
    A = Matrix(mat)
    A.max_cols()
    A.max_rows()
    A.diag_se()
    A.diag_ne()

def level12(): # Not solved
    def triangle_numbers():

        fo.write('\t'.join(map(str, self.SC())))
        fo.write(' ' + str(self.S()))
        S = 1
        i = 1
        while True:
            yield i, S
            i += 1
            S += i

    f = Factoriser(int(1e6))

    for i, n in triangle_numbers():
        if i < 7564: continue
        if True: #n % 10 == 0:
            L = f.do_proper_divisors(n)
            #if len(L) > 200:
            print len(L), '\t', i , n, L
            #print len(L), i



datas = ''' 37107287533902102798797998220837590246510135740250
46376937677490009712648124896970078050417018260538
74324986199524741059474233309513058123726617309629
91942213363574161572522430563301811072406154908250
23067588207539346171171980310421047513778063246676
89261670696623633820136378418383684178734361726757
28112879812849979408065481931592621691275889832738
44274228917432520321923589422876796487670272189318
47451445736001306439091167216856844588711603153276
70386486105843025439939619828917593665686757934951
62176457141856560629502157223196586755079324193331
64906352462741904929101432445813822663347944758178
92575867718337217661963751590579239728245598838407
58203565325359399008402633568948830189458628227828
80181199384826282014278194139940567587151170094390
35398664372827112653829987240784473053190104293586
86515506006295864861532075273371959191420517255829
71693888707715466499115593487603532921714970056938
54370070576826684624621495650076471787294438377604
53282654108756828443191190634694037855217779295145
36123272525000296071075082563815656710885258350721
45876576172410976447339110607218265236877223636045
17423706905851860660448207621209813287860733969412
81142660418086830619328460811191061556940512689692
51934325451728388641918047049293215058642563049483
62467221648435076201727918039944693004732956340691
15732444386908125794514089057706229429197107928209
55037687525678773091862540744969844508330393682126
18336384825330154686196124348767681297534375946515
80386287592878490201521685554828717201219257766954
78182833757993103614740356856449095527097864797581
16726320100436897842553539920931837441497806860984
48403098129077791799088218795327364475675590848030
87086987551392711854517078544161852424320693150332
59959406895756536782107074926966537676326235447210
69793950679652694742597709739166693763042633987085
41052684708299085211399427365734116182760315001271
65378607361501080857009149939512557028198746004375
35829035317434717326932123578154982629742552737307
94953759765105305946966067683156574377167401875275
88902802571733229619176668713819931811048770190271
25267680276078003013678680992525463401061632866526
36270218540497705585629946580636237993140746255962
24074486908231174977792365466257246923322810917141
91430288197103288597806669760892938638285025333403
34413065578016127815921815005561868836468420090470
23053081172816430487623791969842487255036638784583
11487696932154902810424020138335124462181441773470
63783299490636259666498587618221225225512486764533
67720186971698544312419572409913959008952310058822
95548255300263520781532296796249481641953868218774
76085327132285723110424803456124867697064507995236
37774242535411291684276865538926205024910326572967
23701913275725675285653248258265463092207058596522
29798860272258331913126375147341994889534765745501
18495701454879288984856827726077713721403798879715
38298203783031473527721580348144513491373226651381
34829543829199918180278916522431027392251122869539
40957953066405232632538044100059654939159879593635
29746152185502371307642255121183693803580388584903
41698116222072977186158236678424689157993532961922
62467957194401269043877107275048102390895523597457
23189706772547915061505504953922979530901129967519
86188088225875314529584099251203829009407770775672
11306739708304724483816533873502340845647058077308
82959174767140363198008187129011875491310547126581
97623331044818386269515456334926366572897563400500
42846280183517070527831839425882145521227251250327
55121603546981200581762165212827652751691296897789
32238195734329339946437501907836945765883352399886
75506164965184775180738168837861091527357929701337
62177842752192623401942399639168044983993173312731
32924185707147349566916674687634660915035914677504
99518671430235219628894890102423325116913619626622
73267460800591547471830798392868535206946944540724
76841822524674417161514036427982273348055556214818
97142617910342598647204516893989422179826088076852
87783646182799346313767754307809363333018982642090
10848802521674670883215120185883543223812876952786
71329612474782464538636993009049310363619763878039
62184073572399794223406235393808339651327408011116
66627891981488087797941876876144230030984490851411
60661826293682836764744779239180335110989069790714
85786944089552990653640447425576083659976645795096
66024396409905389607120198219976047599490197230297
64913982680032973156037120041377903785566085089252
16730939319872750275468906903707539413042652315011
94809377245048795150954100921645863754710598436791
78639167021187492431995700641917969777599028300699
15368713711936614952811305876380278410754449733078
40789923115535562561142322423255033685442488917353
44889911501440648020369068063960672322193204149535
41503128880339536053299340368006977710650566631954
81234880673210146739058568557934581403627822703280
82616570773948327592232845941706525094512325230608
22918802058777319719839450180888072429661980811197
77158542502016545090413245809786882778948721859617
72107838435069186155435662884062257473692284509516
20849603980134001723930671666823555245252804609722
53503534226472524250874054075591789781264330331690
'''

def level13():
    S = sum([int(l) for l in datas.splitlines()])
    print str(S)[0:10]

def level14():

    def collatz_sequence(seed):
        n = seed
        i = 1
        while n != 1:
            if n % 2 == 0:
                n /= 2
            else:
                n = 3*n + 1
            i += 1
        return i

    max = -1
    for i in xrange(1,1e6+1):
        res = collatz_sequence(i)
        if res > max:
            max = res
            print i, max

def level15():
    ''' The same problem as in google treasure hunt (which was 
    done after project euler ... but the problem existed before both :)
    '''
    cache = []
    def set_cache_result(n, p, res):
        cache[n][p] = res

    def is_in_cache(n, p):
        return cache[n][p] != -1

    def get_cache_result(n, p):
        return cache[n][p]

    def robot(n, p):

        if n == 1 or p == 1: return 1

        if is_in_cache(n,p):
            return get_cache_result(n,p)

        res = 0
        for j in xrange(1, p+1):
            res += robot(n-1, j)

        return res

    def populate_cache(n, p):

        # init
        for i in xrange(0, n+1):
            L = [-1 for j in xrange(0, p+1)]
            cache.append(L)
        
        for i in xrange(1, n+1):
            for j in xrange(1, p+1):
                res = robot(i,j)
                print i,j,res
                set_cache_result(i,j,res)

    print populate_cache(21, 21)

def level16():
    s = str(2 ** 1000)
    print sum([int(i) for i in s])

def num_to_letters(n):
    one_to_nineteen = ['',
'one',
'two',
'three',
'four',
'five',
'six',
'seven',
'eight',
'nine',
'ten',
'eleven',
'twelve',
'thirteen',
'fourteen',
'fifteen',
'sixteen',
'seventeen',
'eighteen',
'nineteen']

    dizaines = [
'', # nop
'',# nop
'twenty',
'thirty',
'forty',
'fifty',
'sixty',
'seventy',
'eighty',
'ninety'
]
    if n < 20:
        return one_to_nineteen[n]
    elif n >= 20 and n < 100:
        x = n/10
        rem = n % 10
        if rem:
            return dizaines[x] + ' ' + num_to_letters(rem)
        else:
            return dizaines[x]
    elif n >= 100 and n < 1000:
        x = n/100
        rem = n % 100
        if rem == 0:
            return num_to_letters(x) + ' hundred'
        else:
            return num_to_letters(x) + ' hundred and ' + num_to_letters(rem)
    elif n == 1000:
        return 'one thousand'

def level17():
    ''' This is British english for the one hundred and five '''
    S = 0
    max = 1000
    for i in xrange(1,max+1):
        tmp = num_to_letters(i)
        L = len(tmp.replace(' ',''))
        print i, tmp, L
        S += L
    print S

triangle_big = '''75
95 64
17 47 82
18 35 87 10
20 04 82 47 65
19 01 23 75 03 34
88 02 77 73 07 63 67
99 65 04 28 06 16 70 92
41 41 26 56 83 40 80 70 33
41 48 72 33 47 32 37 16 94 29
53 71 44 65 25 43 91 52 97 51 14
70 11 33 28 77 73 17 78 39 68 17 57
91 71 52 38 17 14 91 43 58 50 27 29 48
63 66 04 68 89 53 67 30 73 16 69 87 40 31
04 62 98 27 23 09 70 98 73 93 38 53 60 04 23
'''

triangle_small = '''3
7 5
2 4 6
8 5 9 3
'''

def level18():
    #mat_str = read_input(triangle_small)
    mat_str = read_input(triangle_big)
    print mat_str[0][0]
    N = len(mat_str)

    def triangle_rec(i,j,N):
        if i>N: return 0
        return mat_str[i][j] + max(triangle_rec(i+1, j, N), triangle_rec(i+1, j+1, N))

    print triangle_rec(0,0,N-1)


def level19():
    C = [calendar.monthcalendar(y, m)[0][1] == 1 for y in xrange(1901, 2001) for m in xrange(1,13)]
    print sum([1 if i == True else 0 for i in C])


def level20():
    def fact(n):
        if n == 1: return 1
        else: return n * fact(n -1)
    s = str(fact(100))
    print sum([int(i) for i in s])

def level21():

    D = Factoriser(5)

    tables_amicables = {}
    for i in xrange(1, 10000):
        tables_amicables[i] = D.proper_divisor_sum(i)

    S = 0
    for i in xrange(1, 10000):
        a = tables_amicables[i]
        if a in tables_amicables:
            if tables_amicables[a] == i:
                if a != i:
                    print a, i
                    S += i
    print S

def level22():
    names = [n for n in open('names_level22.txt').read().replace('"','').split(',')]
    names.sort()

    def weight(name): 
        return sum((ord(l) - ord('A') + 1 for l in name))

    print sum((i+1) * weight(n) for i, n in enumerate(names))

def pair_sum(n):
    i = 1
    j = n - 1
    while i <= j:
        yield i,j
        i += 1
        j -= 1

def level23():
    D = Factoriser(5)

    abundant = {}
    for i in xrange(10, 28123 + 1):
        s = D.proper_divisor_sum(i)
        if s > i:
            abundant[i] = s
            print i,s

    def abundant_sumable(n):
        for i,j in pair_sum(n):
            if i in abundant and j in abundant:
                return True
        return False

    print sum(i for i in xrange(1, 28123 + 1) if not abundant_sumable(i))


def permutations(L):
    if len(L) <= 1:
        yield L
    else:
        a = [L.pop(0)]
        for p in permutations(L):
            for i in range(len(p)+1):
                yield p[:i] + a + p[i:]

def level24():
    N = 10
    S = [''.join(str(l) for l in p) for p in permutations(range(0,N))]
    S.sort()
    print S[int(1e6)-1]

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

def level26(): # Not solved

    def divide(a, b):
        precision = 10

        ratio = 10 ** (len(str(b)) - 1) # 10 for i < 10, 100 for i < 100, etc ...
        div = a * ratio

        for i in range(precision):

            mod = div % b
            div /= b

            print div
            # if mod == 0: break

            div = mod * ratio

    regexp = re.compile(r'(\d+)\1')
    def recurring_cycle(i):
        '''
        >>> re.findall(r'(\d)*\1', '32323232')
        ['3232']
        '''
        q = Decimal(1) / Decimal(i)
        a = str(q)[2:]

        length = 1
        found = False
        L = []

        while length:
            res = regexp.findall(a)
            length = len(res)
            #print a, res, found, length
            if length == 0:
                break
            else:
                if found:
                    L.append(res)
                found = True
                a = res[0]

        if found:

            # Try to find the first local maximum
            # [1,2,3,4,5,4,3,3,1,7,8,9] -> 5

            L.reverse()
            
            v_max = -1
            i_max = 0 
            yop = False
            for i,v in enumerate(L):
                #print 'i, v =', i, v
                if v:
                    if len(v) > v_max:
                        v_max = len(v)
                        i_max = i
                        #print 'imax, vmax =', i_max, v_max
                    else:
                        if len(v) < v_max:
                            if v_max != -1:
                                yop = True
                                break

            #print i_max, v_max
            if v_max == -1:
                return None

            if yop: return L[i_max+1][0]
            else: return L[i_max][0]

        else:
            return None

    getcontext().prec = 10000
    assert ( recurring_cycle(2) == None)
    assert ( recurring_cycle(3) == '3')
    assert ( recurring_cycle(7) == '142857')
    assert ( recurring_cycle(101) == '0099')
    assert ( recurring_cycle(91) == '010989')
    assert ( recurring_cycle(77) == '012987')
    print len(recurring_cycle(823))
    assert ( len(recurring_cycle(823)) == 2466 )
    #return

    nb_max = 1000
    all_cycles = []
    for i in xrange(2, nb_max+1):
        R = recurring_cycle(i)
        if R:
            print i, len(R)
        all_cycles.append((R,i))
    all_cycles = [i for i in all_cycles if i[0] != None] # some None elements
    all_cycles.sort(key=lambda x: len(x[0]))
    print all_cycles

def level27():
    
    def quadratic(a, b, n):
        '''n^2 + a.n + b'''
        return n * n + a * n + b

    N = 2e6
    primes_dict = compute_primes_native(N)

    # 1 is not a prime ...
    def is_prime(i): return i in primes_dict

    a, b = 1, 41
    a, b = -79, 1601 
    for k in xrange(40):
        p = quadratic(a, b, k)
        assert(is_prime(p))

    def prod(a,b):
        k = 0
        while True:
            p = quadratic(a, b, k)
            if not is_prime(p):
                break
            k += 1
        return k, a * b

    print prod(a,b)

    k_max = 0
    for a in range(-999, 1000, 1):
        for b in range(-999, 1000, 1):
            k, p = prod(a,b)
            if k > k_max:
                k_max = k
                print k, p

    

def level28():

    def sample(s, Max=0):

        def sample_positive(s, Max=0):
            for i in range(Max):
                if s < float(i+1) / Max:
                    return i
            return Max - 1

        if s > 0:
            return sample_positive(s, Max)
        else:
            return sample_positive(-s, Max) * -1

    assert sample(0.7,2) == 1
    assert sample(0.3,2) == 0

    assert sample(-0.2,3) == 0
    assert sample(-0.5,3) == -1
    assert sample(-0.8,3) == -2

    assert sample(-0.7,2) == -1
    assert sample(-0.3,2) == 0

    assert sample(0.2,3) == 0
    assert sample(0.5,3) == 1
    assert sample(0.8,3) == 2

    def draw_circle(n):
        mat_str = ''' 21 22 23 24 25
20  7  8  9 10
19  6  1  2 11
18  5  4  3 12
17 16 15 14 13'''

        mat = read_input(mat_str)
        N = 7
        mat = [[0 for i in xrange(N)] for j in xrange(N)]
        A = Matrix(mat)
        k = N / 2
        l = N / 2

        from math import cos, sin, pi
        for j in [0,9,25]:

            if j == 0:
                angle_denominator = 4
                max_sample = 2
            elif j == 9:
                angle_denominator = 8
                max_sample = 3
            elif j == 25:
                angle_denominator = 12
                max_sample = 4

            for i in xrange((max_sample+1)**2 ):

                angle = -1 * float(i) * pi / angle_denominator

                c = cos(angle)
                s = sin(angle)

                c_d = sample(c, max_sample)
                s_d = sample(s, max_sample)

                K = k + c_d
                L = l + s_d

                print 'i = %d [%d,%d]' %(i, L, K)
                print 'angle %d*pi/%d(%f) cos %f sin %f' %(i, angle_denominator, angle, c, s)
                print 'sample %d %d' %(c_d, s_d)
                A.m[L][K] = i + j


                print A

        return A

    def draw_spiral():

        N = 7
        mat = [[0 for i in xrange(N)] for j in xrange(N)]
        A = Matrix(mat)

        A.value = N ** 2

        while not A.center():
            A.fill_W()
            A.fill_S()
            A.fill_E()
            A.fill_N()
        print A
        print A.the_diag() + A.the_other_diag() - 1

    draw_spiral()

def level29():
    s = set()
    N = 5
    N = 100
    for a in xrange(2,N+1):
        s = s.union(set(a ** b for b in xrange(2,N+1)))
    print len(s)


def level30():
    N = 4
    N = 5
    Max = N * 9 ** N

    S = 0
    for j in range(2,Max):
        if j == sum(int(i) ** N for i in list(str(j))):
            print j
            S += j

    print 'res =', S

def level31():
    ''' Solution += 1 because 2 pounds = 200p '''

    def coin_sum(p100, p50 = 0, p20 = 0, p10 = 0, p5 = 0, p2 = 0, p1 = 0):
        return p1 * 1 + p2 * 2 + p5 * 5 + p10 * 10 \
            + p20 * 20 + p50 * 50 + p100 * 100

    def is_2pound(p100, p50 = 0, p20 = 0, p10 = 0, p5 = 0, p2 = 0, p1 = 0):
        if coin_sum(p100, p50, p20, p10, p5, p2, p1) == 200:
            print p100, p50, p20, p10, p5, p2, p1
            return True
        return False

    def over_2pound(p100, p50 = 0, p20 = 0, p10 = 0, p5 = 0, p2 = 0, p1 = 0):
        return coin_sum(p100, p50, p20, p10, p5, p2, p1) > 200
        
    assert (is_2pound(1, 1, 2, 0, 1, 1, 3))
    assert (over_2pound(2, 1))

    i = 0
    for p100 in range(2):
        for p50 in range(4):
            if over_2pound(p100, p50): break
            for p20 in range(10):
                if over_2pound(p100, p50, p20): break
                for p10 in range(20):
                    if over_2pound(p100, p50, p20, p10): break
                    for p5 in range(40):
                        if over_2pound(p100, p50, p20, p10, p5): break
                        for p2 in range(100):
                            if over_2pound(p100, p50, p20, p10, p5, p2): break
                            for p1 in range(200):
                                if over_2pound(p100, p50, p20, p10, p5, p2, p1): break
                                if is_2pound(p100, p50, p20, p10, p5, p2, p1):
                                    i += 1
    print i + 8 #  1 2pounds

def level32():
    def num_to_chars(x):
        return [i for i in str(x)]

    def is_pandigital(a,b):
        p = a * b

        return len(str(a) + str(b) + str(p)) == 9 and \
                all( \
                [ \
                    str(i) in num_to_chars(a) or \
                    str(i) in num_to_chars(b) or \
                    str(i) in num_to_chars(p) \
                        for i in xrange(1,10)
                ]
            )

    # 10^1 * 10^2 -> 10^3 / 1 + 2 + 3 = 6
    # 6 + 3 = 9

    assert is_pandigital(39, 186)
    pandigitals = []
    prods = []
    # To make sure everything works, use a_max = 40 and b_max = 200 to start
    a_max, b_max = 40, 200
    a_max, b_max = 10000, 10000

    for a_max, b_max in [
            [10, 1000000], 
            [100, 100000], 
            [1000, 10000], 
            [1000,  1000], 
            ]:
        for a in range(a_max):
            for b in range(b_max):
                p = a * b
                if len(str(a) + str(b) + str(p)) > 9: break

                if not p in prods:
                    if is_pandigital(a,b):
                        pandigitals.append( [a,b,p] )
                        prods.append(p)

    print pandigitals
    print sum(prods)

def level33():
    getcontext().prec = 100

    def fake_simplified(n, d):
        n1 = n / 10
        n2 = n % 10
        d1 = d / 10
        d2 = d % 10

        if n2 == 0 or n1 == 0: return False
        if d2 == 0 or d1 == 0: return False

        q_real = Decimal(n) / Decimal(d)
        if n1 == d2:
            q_fake = Decimal(n2) / Decimal(d1)
            return q_real == q_fake
        elif n1 == d1:
            q_fake = Decimal(n2) / Decimal(d2)
            return q_real == q_fake
        elif n2 == d1:
            q_fake = Decimal(n1) / Decimal(d2)
            return q_real == q_fake
        elif n2 == d2:
            q_fake = Decimal(n1) / Decimal(d1)
            return q_real == q_fake
        else:
            return False

    assert fake_simplified(49, 98)
    assert fake_simplified(48, 98) == False
    assert fake_simplified(50, 60) == False

    for a in range(10,100):
        for b in range(10,100):
            if a >= b: continue # only numbers < 1

            if fake_simplified(a, b):
                print a, '/', b
    # 16 / 64
    # 19 / 95
    # 26 / 65
    # 49 / 98

    N = 16 * 19 * 26 * 49
    D = 64 * 95 * 65 * 98

    print N, D
    # 387296 38729600
    # answer equals D when N / D is simplified -> answer = 100

def level34():

    def fact(n):
        res = 1
        while n > 1:
            res *= n
            n -= 1
        return res

    all_fact = {}
    for i in range(10):
        all_fact[i] = fact(i)

    Max = 5 * fact(9)

    S = 0
    for j in range(2,Max):
        if j == sum(all_fact[int(i)] for i in list(str(j))):
            print j
            S += j

    print 'res =', S


def rotate(tmp):
    '''
    This works too l.insert(0,l.pop())
    '''
    for i in range(len(tmp)): 
        tmp = [tmp[-1]] + tmp[:-1]
        yield int(''.join(tmp))

def level35():
    N = 1000000
    primes = compute_sorted_primes(N)
    primes_dict = compute_primes_native(N)

    # 1 is not a prime ...
    def is_prime(i): return i in primes_dict

    Lp = []
    for p in primes:
        if p <= 10:
            continue

        tmp = list(str(p))
        if '0' in tmp:
            continue

        if all(is_prime(i) for i in rotate(tmp)):
            print p
            Lp.append(p)

    print 'res', len(Lp + [2,3,5,7])


def level36():
    ''' Computing the list of candidates is useless / checking
    both properties at the same time is equally fast'''
    def base2(val):
        out = ''
        while val:
            out = str( val & 1 ) + out
            val >>=1
        return out

    Max = int(1e6)

    candidates = (i for i in range(1,Max+1) if is_palindrome(i))

    S = 0
    for c in candidates:
        if is_palindrome(base2(c)):
            print c, base2(c)
            S += c

    print 'res =', S

def level37():
    N = 1000000
    primes = compute_sorted_primes(N)
    primes_dict = compute_primes_native(N)

    # 1 is not a prime ...
    def is_prime(i): return i in primes_dict

    Lp = []
    for p in primes:
        if p <= 7:
            continue
        S = str(p)

        '''>> ['3', '37', '379', '3797']'''
        trunc_left = [S[:i] for i in xrange(1,len(S)+1)]

        '''>> ['3797', '797', '97', '7'] '''
        trunc_right = [S[i:] for i in xrange(0,len(S))]

        t = trunc_left + trunc_right
        if all(is_prime(int(i)) for i in t):
            print p, t
            Lp.append(p)

    print 'res', sum(Lp)
    print 'res (11)', Lp[0:11], sum(Lp[0:11])
    print 'res (:11)', Lp[-11:], sum(Lp[-11:])

def level38():
    def num_to_chars(x):
        return [i for i in str(x)]

    def is_pandigital(a):
        return all( str(i) in num_to_chars(a) for i in xrange(1,10) )

    assert is_pandigital('192384576')

    # for M in [9, 192]:
    # Born max = 1e9
    pans = []
    for M in xrange(int(1e9)):
        s = ''
        i = 1
        while len(s) < 9:
            s += str(M * i)
            i += 1
        if is_pandigital(s) and len(s) == 9:
            pans.append(s)
            print M, s

    # let it run for a while, and the last one it prints is the good one

def level39():

    from math import sqrt, modf
    perimeters = {}
    # First try with t_max = 122
    for p in range(1000):
        print p
        for a in range(1,p):
            for b in range(a,p):
                c = sqrt(a*a + b*b)
                if modf(c)[0] != 0.0: continue
                c = int(c)
                if a+b+c == p:
                    v = perimeters.get(p, 0) 
                    perimeters[p] = v + 1
                    print a, b, c
    print perimeters
    L = [[v, k] for k,v in perimeters.iteritems()]
    L.sort()
    print L
    # sol: 840 ?
                        
def level40():
    N = int(21)
    N = int(1e6)
    d = ''.join((str(i) for i in xrange(1,N)))

    print d[11] # 12th digit
    print d[10] # 12th digit

    factors = (int(d[-1 + 10 ** i]) for i in xrange(6+1))
    print reduce(lambda x,y: x*y, factors)

def level41(): # Not solved
    def num_to_chars(x):
        return [i for i in str(x)]

    def is_n_pandigital(a, n = 9):
        return len(str(a)) == n and \
                all( str(i) in num_to_chars(a) for i in xrange(1,n+1) )

    assert is_n_pandigital('192384576')
    assert is_n_pandigital('1324', 4)
    assert is_n_pandigital('13247568', 8)
    assert not is_n_pandigital('124', 4)

    N  = int(1e8)
    primes_dict = compute_primes_native(N)

    n_max = 2
    for p in sorted(primes_dict.keys()):
        for n in range(n_max,9+1):
            if is_n_pandigital(p, n):
                n_max = n
                print p, n
    # 7652413 ?

def level42():

    def is_triangle_number(n):
        S = 1
        i = 1
        while S < n:
            i += 1
            S += i
        return S == n

    assert is_triangle_number(1)
    assert is_triangle_number(3)
    assert is_triangle_number(6)
    assert is_triangle_number(21)
    assert not is_triangle_number(25)
    assert is_triangle_number(28)
    assert is_triangle_number(55)

    words = open('words.txt').read()[:-1].replace('"','').split(',')

    def lweight(letter):
        return ord(letter) - ord('A') + 1

    def triangle_weight(index):
        return index

    def wweight(word):
        return sum( lweight(l) for l in word )

    # SKY is 19 + 11 + 25 = 55 = t10
    assert wweight('SKY') == 55
    print sum([1 for w in words if is_triangle_number(wweight(w))])

def level44(): # Not solved

    # 1, 5, 12, 22, 35, 51, 70, 92, 117, 145, ...

    N = 10 ** 6
    pentagonal = [-1] * N
    pentagonal_dict = {}
    for i in xrange(N):
        p = i * (3*i - 1) / 2
        pentagonal[i] = p 
        pentagonal_dict[p] = None

    assert 1 in pentagonal_dict
    assert 5 in pentagonal_dict
    assert 12 in pentagonal_dict
    assert 22 in pentagonal_dict
    assert not 23 in pentagonal_dict

    res = []
    j_max, k_max = 10000, 10000
    for j in range(1, j_max):
        for k in range(j+1, k_max):
            pk = pentagonal[k]
            pj = pentagonal[j]
            S = pj + pk
            if S in pentagonal_dict:
                #print j,k
                #print 'S', S
                D = pk - pj
                #print 'D', D
                if D in pentagonal_dict:
                    D_abs = abs( pj - pk )
                    print j, k, S, D, D_abs

def level45():

    def pentagonal(n):
        return n * (3*n - 1) / 2

    def is_pentagonal(n):
        S = 1
        i = 1
        while S < n:
            S = pentagonal(i)
            i += 1
        return S == n

    def hexagonal(n):
        return n * (2*n - 1)

    def is_hexagonal(n):
        S = 1
        i = 1
        while S < n:
            S = hexagonal(i)
            i += 1
        return S == n

    def triangle_numbers():
        S = 1
        i = 1
        while True:
            yield S
            i += 1
            S += i

    for i, t in enumerate(triangle_numbers()):
        if i > 284 and is_pentagonal(t) and is_hexagonal(t):
            print i, t 
            return 

    # bash-3.2$ ./euler.py
    # 55384 1533776805
    # Time taken (seconds) = 877.720000

def level47(): # Not solved
    N  = 100000
    N1 = 100000
    primes_dict = compute_primes_native(N)
    f = Factoriser(N)

    # 1 is not a prime ...
    def is_prime(i): 
        print i, 'is prime ?'
        return i in primes_dict

    print f.do_factorize_primal_factors(644)
    print f.do_factorize_primal_factors(645)
    print f.do_factorize_primal_factors(646)

    for i in xrange(N1):
        if is_prime(i) or is_prime(i+1) or is_prime(i+2) or is_prime(i+3):
            continue

        A = f.do_factorize_primal_factors(i)
        B = f.do_factorize_primal_factors(i+1)
        C = f.do_factorize_primal_factors(i+2)
        D = f.do_factorize_primal_factors(i+3)

        if len(A) == len(B) == len(C) == len(D) == 4:
            print 'youpi'
            all = A + B + C + D
            if len(set(all)) == len(all):
                print i,A,B,C,D

def level48():
    S = sum([i ** i for i in xrange(1,1001)])
    print str(S)[-10:]

def level49():
    x = 4
    N  = 10 ** x
    primes = compute_sorted_primes(N)
    primes_dict = compute_primes_native(N)

    # 1009 is the first prime above 1000, index 168
    # 9973 is the last prime below 10000, 
    for i, p in enumerate(primes):
        if p > 1000: 
            #print primes[i]
            #print i
            break

    def same_digits(a, b):
        return set(str(a)) == set(str(b))

    Lp = len(primes)
    for j in xrange(168,Lp):
        inc = 3330
        p1 = primes[j]
        p2 = p1 + inc
        p3 = p1 + inc + inc
        if p1 in primes_dict and p2 in primes_dict and p3 in primes_dict \
            and same_digits(p1, p2) and same_digits(p1, p3):
            print 'res:', p1, p2, p3
            print ''.join(map(str, [p1,p2,p3]))

def level50():
    x = 6
    N  = 10 ** x
    primes = compute_sorted_primes(N)
    primes_dict = compute_primes_native(N)

    if False: # does not work ... guess why ...
        L_max = 1
        for j in xrange(0, len(primes)):
            for k in xrange(j+1, len(primes)):
                # print j,k
                if k - j + 1 < L_max: continue
                s = primes[j:k]

                if len(s) >= L_max and sum(s) in primes_dict:
                    print sum(s), len(s)
                    L_max = len(s)
    else:
        L_max = 1
        Lp = len(primes)

        for j in xrange(0, Lp):
            S = primes[j] 
            #print 'top'
            for k in xrange(j+1, Lp):
                L = k - j + 1

                S += primes[k]

                if S > N: break

                if L > L_max and S in primes_dict:
                    print S, L
                    L_max = L

def level52():
    ''' permutations '''
    def same_digits(a, b):
        return set(str(a)) == set(str(b))

    i = 1
    while True:
        if same_digits(i, 2*i) and \
            same_digits(i, 3*i) and \
            same_digits(i, 4*i) and \
            same_digits(i, 5*i) and \
            same_digits(i, 6*i):
            print i
            break
        i += 1

def level53():
    cnr_table = []
    N = R = 100+1
    for i in xrange(0, N):
        L = [-1 for j in xrange(0, R)]
        cnr_table.append(L)

    @memoize
    def fact(n):
        if n == 1 or n <= 0: return 1
        else: return n * fact(n -1)

    for r in xrange(0, R):
        for n in xrange(r+1, N):
            cnr_table[n][r] = fact(n) / (fact(r) * fact (n-r))

    print cnr_table[23][10]
    print sum(1 for r in xrange(0, R) for n in xrange(r+1, N) \
            if cnr_table[n][r] > 10 ** 6)



# Level 76
def pair_rewrite(n):
    i = 1
    j = n - 1

    while i <= j:
        yield i,j
        i += 1
        j -= 1

from bisect import insort
dico_all = {}

def rewrite_list(n, L, N, verbose):

    insort(L,n)

    if sum(L) == N:
        key = ('').join([str(i) for i in L]) # key is a string
        if not key in dico_all:
            dico_all[key] = len(L)
            if verbose:
                print 'L', L, len(dico_all) - 1

    L.remove(n)

    for i,j in pair_rewrite(n):

        insort(L,j)
        #print 'Cand_i:', L, n, i
        rewrite_list(i, L, N, verbose)
        L.remove(j)

        insort(L,i)
        #print 'Cand_j:', L, n, j
        rewrite_list(j, L, N, verbose)
        L.remove(i)

def rewrite_int(n, S):

    if n + S == 20:
        print 'youpi'

    for i,j in pair_rewrite(n):

        rewrite_int(i, S + j)
        rewrite_int(j, S + i)

def level76(): # Not solved
    if False:
        print 'Test'
        for i,j in pair_rewrite(-5):
            print i,j
        print 'toto'
        import sys
        sys.exit(0)

    def rewrite(N, verbose = False):
        rewrite_list(N, [], N, verbose)
        del dico_all[str(N)]

        if False:
            B = []
            for i in dico_all.keys():
                t = list(i)
                t.reverse()
                B.append(''.join(t))

            if verbose: print B
            A = [(len(i), str(i), i) for i in B]
            A.sort()

        l = 0
        dico = {}
        for k in dico_all.keys():
            l = dico_all[k]
            v = dico.get(l, 0) 
            dico[l] = v + 1

        #print dico
        L = ['%3d' % dico[k] for k in dico.keys()]
        L.reverse()
        res = ' '.join(L)

        dico_all.clear()
        return res

    # Show one example solved
    N = 10 
    print '[%2d]' % N, rewrite(N, verbose = True)

    # Show the triangle
    Range = 22
    for N in xrange(Range):
        print '[%2d]' % N, rewrite(N)

    #rewrite_int(N, 0)


if __name__ == '__main__':
    start = clock()

    # Just in case, to kill the process
    from os import getpid
    pid_fd = open('pid.euler', 'w')
    pid_fd.write(str(getpid()))
    pid_fd.close()

    level53()

    # def level answers to be submited: 
    print "Time taken (seconds) = %.6f" % (clock()-start)

# Try those: 46, 48, 52, 76
# 33, 45, 46, 55

# Next: 29 ?
# Do-able: the spiral: 28
# 1 /d : 26

# 165 does not look too hard for such a big number

# http://projecteuler.net/
