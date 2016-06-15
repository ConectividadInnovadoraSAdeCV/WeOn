
sleep 15
chmod 7777 -R /etc/weon
chmod -R 7777 /dev/ttyS0
/home/rock/WeOn/config/iptables.sh

/home/rock/WeOn/bin/Demonio.o &
