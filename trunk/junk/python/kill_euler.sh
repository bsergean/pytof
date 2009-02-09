#!/bin/sh

pidfile=pid.euler
kill `cat $pidfile`
rm -f $pidfile
