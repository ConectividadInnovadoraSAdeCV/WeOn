
sleep 15
chmod 7777 -R /etc/weon
chmod -R 7777 /dev/ttyS0
/home/rock/WeOn/config/iptables.sh

/home/rock/WeOn/bin/Demonio.o &

sudo mkdir  /var/run/weon_daemon
chmod 777 -R /var/run/weon_daemon

echo 166 > /sys/class/gpio/export
