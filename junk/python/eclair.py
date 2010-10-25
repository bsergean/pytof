#!/usr/bin/env python
import os, sys, zlib
from time import clock

def deflate(fn, files):
    fo = open(fn, 'w')

    buffers = []
    for f in files:
        if os.path.isfile(f) and not os.path.islink(f):
            print 'deflate', f
            try:
                bytes = open(f).read()
                buffer = zlib.compress(bytes)
            except IOError:
                continue
            buffers.append( (f, len(bytes), len(buffer), buffer) )

    header = []
    header.append( str(len(buffers)) )
    for buf_tuple in buffers:
        f, len_uncompressed, len_compressed, buf = buf_tuple
            
        header.append(f)
        header.append(str(len_uncompressed))
        header.append(str(len_compressed))

    fo.write('\n'.join(header) + '\n')
    for buf_tuple in buffers:
        _, _, _, buf = buf_tuple

        fo.write(buf)

    fo.close()

# 49% inflateBack / 9% adler32 / 26% write_nocancel
def inflate(fn):
    fo = open(fn)
    file_count = int(fo.readline())

    header = []
    for _ in xrange(file_count):
        f = fo.readline()[:-1]
        len_uncompressed = int(fo.readline())
        len_compressed = int(fo.readline())

        header.append( (f, len_uncompressed, len_compressed) )

    for i in xrange(file_count):
        f, len_uncompressed, len_compressed = header[i]
        print 'inflate', f

        bytes = fo.read(len_compressed)
        fw = open(f, 'w')
        fw.write( zlib.decompress(bytes) )
        fw.close()

if __name__ == '__main__':
    start = clock()

    argv = sys.argv
    if len(argv) == 1:
        print 'Incorrect use'
    elif len(argv) == 2:
        inflate(sys.argv[1])
    else:
        deflate(sys.argv[1], sys.argv[2:])

    print "Time taken (seconds) = %.6f" % (clock()-start)
