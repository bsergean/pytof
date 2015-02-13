#!/bin/sh
set -v

6g helloworld.go  # compile; object goes into helloworld.6
6l helloworld.6   # link; output goes into 6.out
./6.out
