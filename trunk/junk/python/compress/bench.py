
from random import randint, random
from time import time
from os.path import getsize
import gzip
import struct

# Context manager
class Benchmark(object):
    def __init__(self, name):
        self.name = name
    def __enter__(self):
        self.start = time()
    def __exit__(self, ty, val, tb):
        end = time()
        print("%s : %0.3f seconds" % (self.name, end-self.start))
        return False

def scene(N):
    buffer = []
    for i in xrange(N):
        buffer.append( struct.pack('iii', randint(0, N), randint(0, N), randint(0,N)) )
    out = ''.join(buffer)

    buffer = []
    for i in xrange(N):
        buffer.append( struct.pack('d', random()) )
    out = ''.join(buffer)

    return out
    
N = 100 * 1000
buf = scene(N)
print len(buf) / 1024, 'KB'

with Benchmark('raw'):
    with open('/tmp/foo', 'w') as f:
        f.write(buf)

with Benchmark('gzip'):
    fn = '/tmp/foo.gz'
    f = gzip.open('/tmp/foo.gz', 'w')
    f.write(buf)
    f.close()
    print getsize(fn) / 1024
