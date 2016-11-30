
echo 166 > /sys/class/gpio/export
ifup gprs
service apache2 start
sleep 30

chmod 7777 -R /usr/local/squid/var/logs/
chmod 7777 -R /usr/local/squid/var/run/
chmod -R 7777 /dev/ttyS0
/home/rock/WeOn/config/iptables.sh

#/home/rock/WeOn/bin/weon_mac_service &
/usr/local/squid/sbin/squid
sudo mkdir  /var/run/weon_daemon
chmod 777 -R /var/run/weon_daemon

DATE_TODAY=`date +"%Y-%m-%d"`

check_date_today

service weon_daemon start


check_date_today(){
    if [[ "${DATE_TODAY}" == "*2011*" ]];then
        service ntp restart
        echo ${DATE_TODAY}
        sleep 20
        DATE_TODAY=`date +"%Y-%m-%d"`
        check_date_today
    else
        return
    fi
}
