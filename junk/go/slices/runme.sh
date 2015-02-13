#!/bin/sh

6g slices.go  # compile; object goes into helloworld.6
6l slices.6   # link; output goes into 6.out
./6.out $@
