#!/usr/bin/env python
import os, sys, zlib

def deflate(fn, files):
    fo = open(fn, 'w')

    buffers = []
    for f in files:
        if os.path.isfile(f):
            bytes = open(f).read()
            buffer = zlib.compress(bytes)
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

        bytes = fo.read(len_compressed)
        fw = open(f, 'w')
        fw.write( zlib.decompress(bytes) )
        fw.close()

if __name__ == '__main__':
    inflate(sys.argv[1])
    # deflate(sys.argv[1], sys.argv[2:])
