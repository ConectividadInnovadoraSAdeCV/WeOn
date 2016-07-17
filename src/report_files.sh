#!/bin/bash

BUS=$1

YESTERDAY=`date +"%Y-%m-%d" -d "yesterday"`
LOG_PATH="/home/rock/WeOn/logs"
URL_FILE="${LOG_PATH}/${DATE}-URL.txt"
CONNECTS_FILE="${LOG_PATH}/${DATE}-Connects.txt"
GPS_FILE="${LOG_PATH}/${DATE}-GPS.txt"

REPORT_FILE="${LOG_PATH}/report.txt"

STATUS=`cat ${REPORT_FILE}`
DATE_TODAY=`date +"%Y-%m-%d"`
echo $STATUS
echo $DATE_TODAY

check_date(){
    if [[ "${DATE_TODAY}" == "*2011*" ]];then
        echo $DATE_TODAY
        service ntp restart
        ntpdate 129.6.15.28
        sleep 20
    else
        echo "unable to change date to bus" > fail.log
        curl -T fail.log ftp://ftp.smarterasp.net/Logs/Bus/$BUS/ -u weonweon:weonweon
        sleep 30
        check_date
    fi
}
check_date_today(){
    if [[ "${DATE_TODAY}" == "*2011*" ]];then
        service ntp restart
        echo ${DATE_TODAY}
        sleep 20
        check_date_today
    else
        return
    fi
}

if [[ ${STATUS} == *${DATE_TODAY}* ]]
then
    check_date_today
    exit
else
    check_date
    sleep 30 

    cp  "${LOG_PATH}/squid.log" "${LOG_PATH}/squid.log.${DATE_TODAY}"
    cat "${LOG_PATH}/squid.log" | perl -p -e 's/ (..\/...\/.....(.*) .*)/ \2/g'  | sed 's/ / \| /g' > ${URL_FILE}
    cat "${LOG_PATH}/register.txt" | sed 's/1$/Hombre/g' | sed 's/0$/Mujer/g' > ${CONNECTS_FILE}

    if [ -e "${LOG_PATH}/squid.log" ]
    then
    	curl -T ${URL_FILE} ftp://ftp.smarterasp.net/Logs/Bus/$BUS/ -u weonweon:weonweon
    	rm  "${LOG_PATH}/squid.log"
    fi
    if [ -e "${LOG_PATH}/register.txt" ]
    then 
   	curl -T ${CONNECTS_FILE} ftp://ftp.smarterasp.net/Logs/Bus/$BUS/ -u weonweon:weonweon
   	rm "${LOG_PATH}/register.txt"
    fi
	curl -T ${GPS_FILE} ftp://ftp.smarterasp.net/Logs/Bus/$BUS/ -u weonweon:weonweon
	echo ${DATE_TODAY} > ${REPORT_FILE}

    touch "${LOG_PATH}/squid.log"
    chmod 7777 -R  "${LOG_PATH}/squid.log"
    reboot
fi
