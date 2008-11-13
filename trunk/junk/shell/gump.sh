#!/bin/sh

# Mimic hg forest for some commands (pull / diff)

# About the $repos list
# Use find . -type d -name .hg to find the list of repos, from the prefix of a path where hg forest did succeed. 
# Remove the first one

fatal() {
  echo $@
  exit 1
}

#repos=`cat ../cubicweb_full_hg_repos.txt`
repos=`cat ../cubicweb_public_hg_repos.txt`
test -d yams || fatal "Exec me in the topmost directory"

# helpers
log() {
  echo [gump] $@
}

usage() {
    cat <<EOF
Usage:gump.sh [-slh]
 -h | Display this help message
 [WRITEME]
EOF
    exit 1
}

# Parse arguments
set -- `GETOPT_COMPATIBLE=1 getopt ludh $*` 
PUSH=
PULL=
DIFF=
while [ $1 != -- ]
do
        case $1 in
        -l)
		PULL=yes
		;;
        -u)
		PUSH=yes
		;;
        -d)
		DIFF=yes
		;;
        -h)
		usage
		;;
        esac
        shift   # next flag
done
shift   # skip --

for r in $repos
do
	cd $r

	test -z "$PUSH" || hg push
	test -z "$PULL" || hg pull
	test -z "$DIFF" || hg diff

	cd -
done
