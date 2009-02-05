#!/bin/sh

i=200
while test ! $i = 230
do
	url="http://projecteuler.net/index.php?section=problems&id="
	i=`expr $i + 1`
	curl -o level$i.html $url$i
done
