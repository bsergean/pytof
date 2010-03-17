#!/usr/bin/env python

import sys
fn = 'puzzle1.in' if len(sys.argv) == 1 else sys.argv[1]

cset = set()
machines = {}

for line in open(fn):
    machine, c1, c2, price = line.strip().split()
    cset.add(c1)
    cset.add(c2)
    machines[machine] = (c1, c2, price)

print cset
print machines
