#!/usr/bin/env python
import StringIO, os, time, random, sys

def read_input(fn):
    lines = [l for l in open(fn).read().splitlines()]
    mat = [map(int, l.split()) for l in lines]
    return mat

def random_true_or_false():
    return random.random() > 0.5

def min_index(s):
    m = min(s)
    for i,v in enumerate(s):
        if v == m: return i

class Matrix:
    def __init__(self, m):
        self.m = m

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
        while True:
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

    # pick the minimum
    def solve_minimum_pick(self):

        while True:
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
                    self.flip_col(x)
                    continue

            print
            print self

            if self.positive(): break
        
fn = 'simple.txt'
fn = 'input.txt'
A_input = read_input(fn)
A = Matrix(A_input)

if __name__ == "__main__":
    
    print A.col(3)
    print A.cols()
    print A.SR()
    print A.SC()
    print A.S()
    print A

    #A.solve_total_random_walk()
    #A.solve_random_walk_grow()
    A.solve_minimum_pick()

