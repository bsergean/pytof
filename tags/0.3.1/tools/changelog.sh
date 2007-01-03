#!/bin/sh

test -d tools || {
    echo Should be executed from the trunk dir
    exit 1
}

tget=../wiki/Changelog.wiki

cat > $tget <<EOF
#summary Automatically generated changelog

{{{
EOF

svn log --verbose >> $tget
echo '}}}' >> $tget