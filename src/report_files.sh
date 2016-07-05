#!/bin/bash 

DATE=`date +"%Y-%m-%d" -d "yesterday"`
LOG_PATH="/home/rock/WeOn/logs"
URL_FILE="${LOG_PATH}/${DATE}-URL.txt"
CONNECTS_FILE="${LOG_PATH}/${DATE}-Connects.txt"
GPS_FILE="${LOG_PATH}/${DATE}-GPS.txt"

REPORT_FILE="${LOG_PATH}/report.txt"
STATUS=`cat ${REPORT_FILE}`
DATE_TODAY=`date +"%Y-%m-%d"`
echo $STATUS
echo $DATE_TODAY

if [[ ${STATUS} == *${DATE_TODAY}* ]]
then
    exit
else
    #cat "${LOG_PATH}/squid.log" | perl -p -e 's/ (..\/...\/.....(.*) .*)/ \2/g'  | sed 's/ / \| /g' > ${URL_FILE}
    #cat "${LOG_PATH}/register.txt" | sed 's/1$/Hombre/g' | sed 's/0$/Mujer/g' > ${CONNECTS_FILE}

    if [ -e "${LOG_PATH}/squid.log" ]
    then
    	curl -T ${URL_FILE} ftp://ftp.smarterasp.net/Logs/Bus/1001/ -u weonweon:weonweon
    	rm  "${LOG_PATH}/squid.log"
    fi
    if [ -e "${LOG_PATH}/register.txt" ]
    then 
   	curl -T ${CONNECTS_FILE} ftp://ftp.smarterasp.net/Logs/Bus/1001/ -u weonweon:weonweon
   	rm "${LOG_PATH}/register.txt"
    fi
	curl -T ${GPS_FILE} ftp://ftp.smarterasp.net/Logs/Bus/1001/ -u weonweon:weonweon
	echo ${DATE_TODAY} > ${REPORT_FILE}
fi
