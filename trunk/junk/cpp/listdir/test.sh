dir=/private/tmp
dir=~/src/foss
time find $dir > /tmp/0
g++ -O3 find.cpp && time ./a.out $dir > /tmp/1

diff -q /tmp/1 /tmp/0
