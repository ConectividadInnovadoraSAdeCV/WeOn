#!/bin/bash

BUS=$1

YESTERDAY=`date +"%Y-%m-%d" -d "yesterday"`
DATE_TODAY=`date +"%Y-%m-%d"`

LOG_PATH="/home/rock/WeOn/logs"
REPORT_FILE="${LOG_PATH}/report.txt"
STATUS=`cat ${REPORT_FILE}`

echo $STATUS >> log.date
echo $DATE_TODAY >> log.date

check_date(){
    if [[ "${DATE_TODAY}" == "*2011*" ]];then
        echo $DATE_TODAY
        echo "unable to change date to bus" > fail.log
        curl -T fail.log ftp://ftp.smarterasp.net/Logs/Bus/$BUS/ -u weonweon:weonweon

        service ntp restart

        #ntpdate 129.6.15.28
        sleep 45
        check_date
    fi

    if [[ "${YESTERDAY}" == "*2010*" ]];then
        service ntp restart
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

DATA_USAGE(){
    TOTAL_DATA=`awk '{sum+=$1} END {print sum}' $1`
    RESULT_HM=`echo $TOTAL_DATA | awk '{ split( "B KB MB GB" , v  ); s=1; while( $1>1024  ){ $1/=1024; s++  } print int($1) v[s]  }'`
    DATE_REPORT=`date +"%Y-%m-%d %H:%M:%S"`
    echo "${RESULT_HM} | ${DATE_REPORT}" > $1
}

if [[ ${STATUS} == *${DATE_TODAY}* ]]
then
    check_date_today
    exit
else
    check_date
    sleep 30
    YESTERDAY=`date +"%Y-%m-%d" -d "yesterday"`
    DATE_TODAY=`date +"%Y-%m-%d"`
    URL_FILE="${LOG_PATH}/${YESTERDAY}-URL.txt"
    CONNECTS_FILE="${LOG_PATH}/${YESTERDAY}-Connects.txt"
    GPS_FILE="${LOG_PATH}/${YESTERDAY}-GPS.txt"
    DATA_FILE="${LOG_PATH}/${YESTERDAY}-DATA.txt"


    cp  "${LOG_PATH}/squid.log" "${LOG_PATH}/squid.log.${YESTERDAY}"
    cat "${LOG_PATH}/squid.log" | perl -p -e 's/ (..\/...\/.....(.*) .*)/ \2/g'  | sed 's/ / \| /g' | grep http:/ | perl -p -e 's/ ((http:\/\/.+?\/)\w.*) / \2 | /g' | sort | uniq > ${URL_FILE}

    if [ -e "${LOG_PATH}/squid.log" ]
    then
        curl -T ${URL_FILE} ftp://ftp.smarterasp.net/Logs/Bus/$BUS/ -u weonweon:weonweon
        rm  "${LOG_PATH}/squid.log"
    fi
        
    sed -i 's/0$/Mujer/g' ${CONNECTS_FILE}
    sed -i 's/1$/Hombre/g' ${CONNECTS_FILE}

    DATA_USAGE $DATA_FILE

    curl -T ${DATA_FILE} ftp://ftp.smarterasp.net/Logs/Bus/$BUS/ -u weonweon:weonweon
    curl -T ${CONNECTS_FILE} ftp://ftp.smarterasp.net/Logs/Bus/$BUS/ -u weonweon:weonweon
    curl -T ${GPS_FILE} ftp://ftp.smarterasp.net/Logs/Bus/$BUS/ -u weonweon:weonweon
    echo ${DATE_TODAY} > ${REPORT_FILE}

    touch "${LOG_PATH}/squid.log"
    chmod 7777 -R  "${LOG_PATH}/squid.log"
    reboot
fi
