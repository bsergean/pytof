#!/bin/sh
# http://code.google.com/p/pytof/wiki/Install

# JPEG
if test ! -f /usr/local/lib/libjpeg.a ; then
    cd jpeg-6b
    sh configure
    make
    sudo mkdir /usr/local/lib /usr/local/include
    sudo cp libjpeg.a /usr/local/lib
    sudo cp *.h /usr/local/include
    cd -
fi

# PIL
cd Imaging-1.1.6
sudo python setup.py install
cd -
