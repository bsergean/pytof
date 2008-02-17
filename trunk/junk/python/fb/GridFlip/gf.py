#!/usr/bin/env python
import StringIO, os, time, random, sys, copy

def read_input(fn):
    lines = [l for l in open(fn).read().splitlines()]
    mat = [map(int, l.split()) for l in lines]
    return mat

def random_true_or_false():
    return random.random() > 0.5

def mk_matrix():
    n = random.randint(1, 40)
    m = random.randint(1, 16)

    mat = []
    for i in range(n):
        tmp = []
        for i in range(m):
            x = random.randint(0, 200)
            if random_true_or_false(): x = -x
            tmp += [x]
        mat.append(tmp)
        
    return mat

class Matrix:
    def __init__(self, m):
        self.m = copy.deepcopy(m)

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

    def SR(self):
        return [sum(r) for r in self.rows()]

    def SC(self):
        return [sum(c) for c in self.cols()]

    def S(self):
        return sum(self.SR()) + sum(self.SC())

    def flip_row(self, r):
        for k in range(self.N):
            self.m[r][k] = -self.m[r][k]
        
    def flip_col(self, c):
        for k in range(self.M):
            self.m[k][c] = -self.m[k][c]

    def __str__(self):
        fo = StringIO.StringIO()
        
        for r, r_sr in zip(self.rows(), self.SR()):
            s = '[ ' + '\t'.join(map(str, r)) + ' ] ' + str(r_sr) + '\n'
            fo.write(s)

        fo.write('\t'.join(map(str, self.SC())))
        fo.write(' ' + str(self.S()))

        return fo.getvalue()

    def positive(self):
        return all( x >= 0 for x in self.SR() ) and \
            all( x >= 0 for x in self.SC() )

    # Total random
    def solve_total_random_walk(self):
        while True:
            if random_true_or_false():
                x = random.randint(0, self.N-1)
                self.flip_col(x)
            else:
                x = random.randint(0, self.M-1)
                self.flip_row(x)

            print
            print self

            if self.positive(): break

    # First one to find a solution
    def solve_random_walk_grow(self):
        iterations = 0
        while True:
            iterations += 1
            old_s = self.S()
            if random_true_or_false():
                x = random.randint(0, self.N-1)
                self.flip_col(x)
                if self.S() < old_s:
                    self.flip_col(x)
                    continue
            else:
                x = random.randint(0, self.M-1)
                self.flip_row(x)
                if self.S() < old_s:
                    self.flip_row(x)
                    continue

            print
            print self

            if self.positive(): break
        
        return self.S(), iterations

    # pick the minimum
    def solve_minimum_pick(self):

        def min_index(s):
            m = min(s)
            for i,v in enumerate(s):
                if v == m: return i

        iterations = 0
        while True:
            iterations += 1
            old_s = self.S()
            sr = self.SR()
            sc = self.SC()
            min_sr = min(sr)
            min_sc = min(sc)

            if min_sr < min_sc:
                i = min_index(sr)
                self.flip_row(i)

                if self.S() < old_s:
                    self.flip_row(i)
                    continue
            else:
                i = min_index(sc)
                self.flip_col(i)

                if self.S() < old_s:
                    self.flip_col(i)
                    continue

            print
            print self

            if self.positive(): break

        return self.S(), iterations

    # pick the biggest negative number
    def solve_max_negative_pick(self):

        def max_negative(s):
            negatives = [i for i in s if i < 0]
            try:
                return max(negatives)
            except ValueError: # max() arg is an empty sequence
                return 1

        def max_negative_index(s):
            negatives = [i for i in s if i < 0]
            try:
                m = max(negatives)
                for i,v in enumerate(s):
                    if v == m: return i
            except ValueError: # max() arg is an empty sequence
                return -1

        iterations = 0
        while True:
            iterations += 1
            old_s = self.S()
            sr = self.SR()
            sc = self.SC()
            mn_sr = max_negative(sr) # mn for Max Negative
            mn_sc = max_negative(sc)

            print mn_sr, mn_sc
            super_min = -10000000000000000000000000
            if mn_sr > 0: mn_sr = super_min
            if mn_sc > 0: mn_sc = super_min
            print mn_sr, mn_sc

            if mn_sr > mn_sc:
                print 'sr'
                i = max_negative_index(sr)
                self.flip_row(i)

                if self.S() < old_s:
                    self.flip_row(i)
                    continue
            else:
                print 'sc'
                i = max_negative_index(sc)
                self.flip_col(i)

                if self.S() < old_s:
                    self.flip_col(i)
                    continue

            print
            print self

            if self.positive(): break

        return self.S(), iterations


def _solve_explore_all(Mat, N, M):

    for i in M:
        M = M[1:]
        Mat.flip_row(i)
        for j in N:
            N = N[1:]
            Mat.flip_col(j)

            if Mat.positive(): 
                print Mat
                print
                print 'OK'
                sys.exit()
                
            _solve_explore_all(Mat, N, M)
            Mat.flip_col(j)

        Mat.flip_row(i)

def solve_explore_all(Mat):
    _solve_explore_all(Mat, range(Mat.N), range(Mat.M)) 
    
    
        
# INPUT
if True:
    fn = 'simple.txt'
    fn = 'input.txt'
    input = read_input(fn)
else:
    input = mk_matrix()

if __name__ == "__main__":
    
    A = Matrix(input)
    #if A.M >=3: print A.col(3) FIXME
    print A.cols()
    print A.SR()
    print A.SC()
    print A.S()
    print A

    #A.solve_total_random_walk() # does not seem to work well, guess why ... :)

    A = Matrix(input)
    try:
        solve_explore_all(A)
    except RuntimeError: print 'RunTime error'
    sys.exit(0)

    if False:
        #A.solve_random_walk_grow()
        #A.solve_minimum_pick()
        A.solve_max_negative_pick()
    else:
        A = Matrix(input)
        s1, i1 = A.solve_random_walk_grow()
        A = Matrix(input)
        s2, i2 = A.solve_minimum_pick()
        A = Matrix(input)
        s3, i3 = A.solve_max_negative_pick()

        print
        print s1, i1
        print s2, i2
        print s3, i3


