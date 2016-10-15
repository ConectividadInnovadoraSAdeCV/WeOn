#!/bin/bash

APACHE=apache2
SQUID=squid
DHCP="dhcp"
INTERFACE="ppp"
NTP="ntp"

check_apache(){
    if pgrep $APACHE &>/dev/null;then
        echo "apache2 service: OK"
    else
        service $APACHE start &>/dev/null
        echo "apache2 service: Fail"
    fi

}

check_squid(){
    if pgrep $APACHE &>/dev/null;then
        squid_processes=`pgrep $SQUID | wc -l`
        if [ $squid_processes -ge 2 ]; then
             echo "squid: OK"
        elif [ $squid_processes -eq 1 ];then
            sleep 20
            squid_processes=`pgrep $SQUID | wc -l`
            if [ $squid_processes -ge 2 ]; then
                echo "squid: OK"
            else
                squid_process=`pgrep $SQUID`
                kill -9 $squid_process
            fi

        else
            /usr/local/squid/sbin/squid
            sleep 45
            echo "squid: Fail"
        fi
    else
        echo "squid: Fail"
    fi

}

check_dhcp(){
   if pgrep $DHCP &>/dev/null;then
        echo "dhcp service : OK"
    else
        service $DHCP start

    fi

}

check_ntp(){
   if pgrep $NTP &>/dev/null;then
        echo "ntp service: OK"
    else
        service $NTP start
    fi


}
check_network_interface(){
    if ifconfig -a ppp0 &>/dev/null;then
        echo "ppp service: OK"
    else
        sleep 10
        if ifconfig -a ppp0 &>/dev/null;then
            echo "ppp service: OK"
        else
            ifup gprs &>/dev/null
            echo "ppp service: Fail"
        fi
    fi
}
check_date_system(){
    if pgrep $NTP &>/dev/null;then
        DATE_TODAY=`date +"%Y-%m-%d"`
        if [[ "${DATE_TODAY}" != "*2011*"  ]];then
            echo "date system: OK"
        else
            service ntp restart
            sleep 30
            echo "date system: Fail"
        fi
    else
        echo "date system: Fail"
    fi
}


check_apache
check_dhcp
check_network_interface
check_ntp
check_squid
check_date_system



