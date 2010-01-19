#!/usr/bin/env python

from pdb import set_trace

def base2(n):
    result = ''
    while n > 0:
        result = str(n % 2) + result
        n = n >> 1

    return result

def base7(n):
    result = ''
    while n > 0:
        result = str(n % 7) + result
        n = n / 7

    return result

def hex2dec(n):
    n = n[::-1]
    result = 0

    todigit = {
        '0': 0,
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        'A': 10,
        'B': 11,
        'C': 12,
        'D': 13,
        'E': 14,
        'F': 15,
    }

    for i, e in enumerate(n):
        result += 16 ** i * todigit[e]
        
    return result

def main():
    print base2(11)
    print base7(16)

    print hex2dec('FFFF')

if __name__ == '__main__':
    main()
