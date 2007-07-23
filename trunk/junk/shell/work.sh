#
# If you have shell variables evaluated within qmake variables,
# it won't work.
# Replace SOURCES = $HOME/foo.c
# with:
# HOME=$$system(echo $HOME)
# SOURCES = $${HOME}/foo.c
#

tmp=/tmp/work.$$
qmake -d -d -d > $tmp 2>&1

# DEBUG 1: SOURCES === 
getVar()
{
egrep 'DEBUG 1: SOURCES' $tmp | tail -n 1 | cut -c 21- | tr -d ':'
egrep 'DEBUG 1: HEADERS' $tmp | tail -n 1 | cut -c 21- | tr -d ':'

# Project file
echo `basename $PWD`.pro
}

getInc()
{
egrep 'DEBUG 1: INCLUDEPATH' $tmp | tail -n 1 | cut -c 26- | tr -d ':'
}
files=`getVar`
incs=`getInc | sed 's/ /,/g'`

gvim --cmd "set path=$incs" $files
