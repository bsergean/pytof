#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import os, sys
import tempfile
from os.path import join, getsize, dirname
from CoreGraphics import *

def go(dn, outputFile, ratio = 3):
    # Divide picture dimensions by 3 by default

    pageRect = CGRectMake (0, 0, 612, 792) 
    c_pdf = CGPDFContextCreateWithFilename (outputFile, pageRect)

    def add(inputFile):
        i = CGImageImport (CGDataProviderCreateWithFilename (inputFile))

        print "Add image \'%s\' size is (%d,%d)" % (inputFile, i.getWidth(), i.getHeight())

        tw = int( i.getWidth() / ratio )
        th = int( i.getHeight() / ratio )
        
        cs = CGColorSpaceCreateDeviceRGB()
        c = CGBitmapContextCreateWithColor(tw, th, cs, (0,0,0,0))

        c.setInterpolationQuality(kCGInterpolationLow)
        newRect = CGRectMake(0, 0, tw, th)
        c.drawImage(newRect, i)

        # TODO - stupid to write that to disk and read back
        # there must be a better way
        tmp = tempfile.mktemp('.jpg')
        c.writeToFile(tmp, kCGImageFormatJPEG)
        resized_im = CGImageImport (CGDataProviderCreateWithFilename (tmp))

        # create an output document to draw the image into
        c_pdf.beginPage (pageRect)
        c_pdf.drawImage (pageRect.inset (72, 72), resized_im)
        c_pdf.endPage ()

    files = os.listdir( dn )
    for fn in files:
        add(join(dn, fn))

    c_pdf.finish ()

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print 'Need one folder full of pictures'
        sys.exit(1)

    folder = sys.argv[1]
    out = dirname(folder) + '.pdf'

    go(folder, out)
    print '%s size: %d' % (out, getsize(out))
    os.system('open %s' % out)
