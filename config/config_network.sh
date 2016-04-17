#!/bin/bash

#config static network for eth0 and wlan0
#The purpose is to remove network-manager from our system, to enable static ip 
#for eth0 and wlan0 interfaces

#Copyright (C) 2015 Barajas D. Paul <Paul.Barajas@linux.com>
SOURCE_PATH=`pwd`
USR_DIR=${HOME}
VIM_DIR="${USR_DIR}/.vim"


sudo -k bash <<EOF

apt-get remove -y network-manager

EOF



