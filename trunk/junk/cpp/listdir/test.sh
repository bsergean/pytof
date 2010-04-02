dir=/private/tmp
dir=~/src/foss
g++ -O3 find.cpp && time ./a.out $dir > /tmp/1
time find $dir > /tmp/0

diff -q /tmp/1 /tmp/0
