#!/bin/sh
set -v

6g json_test.go  # compile; object goes into helloworld.6
6l json_test.6   # link; output goes into 6.out
./6.out
