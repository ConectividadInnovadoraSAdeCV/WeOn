#!/bin/bash

check_service(){
echo $1
if [ $1 -gt 3 ];then
    echo "SQUID : OK"
    exit
fi
}


SQUID_PROCESS=`ps -eaf | grep squid | wc -l`
check_service $SQUID_PROCESS
sleep 30 

SQUID_PROCESS=`ps -eaf | grep squid | wc -l`
check_service $SQUID_PROCESS
sleep 30

SQUID_PROCESS=`ps -eaf | grep squid | wc -l`
check_service $SQUID_PROCESS
sleep 30

SQUID_PROCESS=`ps -eaf | grep squid | wc -l`
check_service $SQUID_PROCESS
sleep 30

/usr/local/squid/sbin/squid &

