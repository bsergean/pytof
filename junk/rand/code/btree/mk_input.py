#!/usr/bin/env python
import random

fd = open('input.txt', 'w')
size = int(10 ** 2)
fd.write( str(size) + ' ' )
L = random.sample(xrange(10000000), size)
fd.write( ' '.join(str(i) for i in L) )
fd.close()

