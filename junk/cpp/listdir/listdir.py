import sys
import os
import stat

d = sys.argv[1]

L = os.listdir(d)
files = [ (os.stat(os.path.join(d, f))[stat.ST_MTIME], f) for f in L ]
files.sort()
# files.reverse()
for a,b in files:
    print a, b
