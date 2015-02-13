#!/usr/bin/env python
''' 
./C.py < sample.in | tee out && diff out sample.out
./C_slow_correct.py < input_real > out && diff -q out output_real_ok && echo OK
'''

'''
5
0 0 2 EA               -> [E, A]
1 QRI 0 4 RRQR         -> [R, I, R]
1 QFT 1 QF 7 FAQFDFQ   -> [F, D, T]
1 EEZ 1 QE 7 QEEEERA   -> [Z, E, R, A]
0 1 QW 2 QW            -> []

Case #1: [E, A]
Case #2: [R, I, R]
Case #3: [F, D, T]
Case #4: [Z, E, R, A]
Case #5: []


'''

import sys
import pdb
from collections import defaultdict

def solve(combines, opposed, elements):
    elements = [i for i in elements]

    # a round
    L = len(elements)
    i = 0
    oppose_found = {}

    while True:
        element = elements[i]
        #print element
        next = False

        # print 'I:', i

        # look up an opposed (first)
        if element in opposed:
            # print 'found opposed:', element
            op = opposed[element]
            #print 'of :', op

            if op in oppose_found:
                # print 'op in oppose_found:', element
                start = oppose_found[op]
                del oppose_found[op]
                next = True
                # print oppose_found
                for j in xrange(i - start + 1):
                    #print 'before', start, j
                    elements.pop(start)
                    #print 'after', elements
                i = start - 1
            else:
                # print 'NO op in oppose_found:', element
                oppose_found[element] = i

        # print elements, 'after oppose search'

        # look up a combine
        if not next:
            if i+1 != L:
                nextElem = elements[i+1]
                pair = element+nextElem
                if pair in combines:
                    # print 'found combine'
                    elements.pop(i)
                    elements.pop(i)
                    elements.insert(i, combines[pair])

        # print elements
        L = len(elements)
        i += 1
        if L == 0 or i == L: break


    return elements

if __name__ == '__main__':
    answers = [
        'NO', 11
    ]
    answers = []

    T = sys.stdin.readline()
    T = int(T)
    for j in xrange(T):
        line = sys.stdin.readline()
        tokens = line.split()

        C = int(tokens[0])
        tokens.pop(0)
        combines = {}
        for i in xrange(C):
            combine = tokens[i]
            combines[ combine[0]+combine[1] ] = combine[2]
            combines[ combine[1]+combine[0] ] = combine[2]

        for i in xrange(C): tokens.pop(0)
        #print combines

        D = int(tokens[0])
        tokens.pop(0)
        #opposed = defaultdict(list)
        opposed = {}
        for i in xrange(D):
            opp = tokens[i]
            #opposed[ opp[0] ].append( opp[1] )
            #opposed[ opp[1] ].append( opp[0] )
            opposed[ opp[0] ] = opp[1]
            opposed[ opp[1] ] = opp[0]

        for i in xrange(D): tokens.pop(0)
        #print opposed

        N = int(tokens[0])
        tokens.pop(0)
            
        elements = tokens[0]

        answer = solve(combines, opposed, elements)
        answer = '[' + ', '.join(answer) + ']'
        output = 'Case #%d: %s\n' % (j+1, answer)
        sys.stdout.write(output)
        sys.stderr.write(output)
        

    
