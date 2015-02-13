#!/bin/sh

6g wiki.go  # compile; object goes into helloworld.6
6l wiki.6   # link; output goes into 6.out
./6.out $@
