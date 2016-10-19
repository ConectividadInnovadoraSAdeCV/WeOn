#!/bin/bash

sudo -k bash <<EOF

apt-get install git terminator

EOF

git config --global user.name "Paul Barajas"
git config --global user.email paul.barajas@linux.com
git config --global core.editor vim
git config --global color.ui true
git config --global color.branch true
git config --global color.diff true
git config --global color.interactive true
git config --global color.status true
git config --global color.diff.meta "blue black bold"

ssh-keygen -t rsa -b 4096 -C "paul.barajas@linux.com"

