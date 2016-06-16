#!/bin/bash

apt-get install python-daemon chkconfig
apt-get install python-serial

mkdir  /var/run/weon_daemon  /var/log/weon_daemon
chmod 755 -R /var/run/weon_daemon
chmod 755 -R /var/log/weon_daemon

cp config/weon_daemon /etc/init.d/
chmod u+x /etc/init.d/weon_daemon
chkconfig testdaemon on
