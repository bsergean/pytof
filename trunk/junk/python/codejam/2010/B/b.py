#!/usr/bin/env python
from pdb import set_trace
from collections import deque
import sys

def run_slow(R, k, G):

    euros = 0

    D = deque(G)
    passengers = deque()
    P = 0

    def lap():
        P = 0
        while True:
            if not D: # D is empty
                break
            p = D.popleft()
            passengers.append(p)
            P += p
            if P > k:
                # on enleve le dernier convoi
                D.appendleft(p)
                passengers.pop()
                return P - p
        return P

    while R > 0:
        P = lap()
        P = 0
        euros += sum(passengers)

        D.extend(passengers)
        passengers.clear()

        R -= 1

    return euros

def run_slow2(R, k, G):

    def lap():
        print 'lap'
        P = 0
        while True:
            p = G[0]
            print p
            G.rotate(-1)
            P += p
            if P > k:
                G.rotate(1)
                return P - p
        return P

    euros = 0
    while R > 0:
        P = lap()
        euros += P
        print 'euros', P
        R -= 1

    return euros

def run(R, k, G):

    def lap(i):
        P = 0
        L = len(G)
        while True:
            p = G[i]
            P += p
            if P > k:
                return P - p, i

            i += 1
            if i == L: i = 0

    euros = 0
    i = 0
    while R > 0:
        P, i = lap(i)
        euros += P
        R -= 1

    return euros

if __name__ == '__main__':
    # assert run(4, 6, [1, 4, 2, 1]) == 21
    # assert run_slow2(4, 6, deque([1, 4, 2, 1])) == 21

    lines = open('in.txt').read().splitlines()
    S = int( lines[0] )
    j = 1
    c = 1
    for i in range(S):

        line = map(int, lines[j].split())
        R = line[0]
        k = line[1]

        if False:
            G = deque()
            for g in lines[j+1].split():
                G.append(int(g))
            sys.stderr.write('%d\n' % c)
            print 'Case #%d: %s' % (c, run_slow2(R, k, G))

        else:
            G = []
            for g in lines[j+1].split():
                G.append(int(g))
            sys.stderr.write('%d\n' % c)
            print 'Case #%d: %s' % (c, run(R, k, G))

        j += 2
        c += 1
