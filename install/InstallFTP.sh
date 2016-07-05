#!/bin/bash

apt-get install aptitude
apt-get install python-daemon
apt-get install python-serial
apt-get install sysv-rc-conf

mkdir  /var/run/weon_daemon  /var/log/weon_daemon
chmod 755 -R /var/run/weon_daemon
chmod 755 -R /var/log/weon_daemon

cp config/weon_daemon /etc/init.d/
chmod u+x /etc/init.d/weon_daemon
sysv-rc-conf weon_daemon on
