#!/usr/bin/env bash

# forest clone the cubicweb mercurial repo
# need bash for cd -

repos=`cat cubicweb_public_hg_repos.txt`
url_prefix="http://www.logilab.org/cgi-bin/hgwebdir.cgi"

prefix=fcubicweb # use your favorite name, but not cubicweb
rm -rf $prefix
mkdir -p $prefix
cd $prefix

for r in $repos
do
	dn=`dirname ${r}`
	bn=`basename ${r}`

	mkdir -p $dn # will be a cd .
	cd $dn

	hg clone $url_prefix/${r}

	cd -
done

