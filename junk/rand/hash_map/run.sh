#!/bin/sh

g++ -m64 -O3 hash_map.cpp chrono.cpp \
	MurmurHash2.cpp \
	MurmurHash2_64.cpp

test $? -eq  0 && ./a.out
