#!/bin/bash
CAMION=$(head /etc/weon/CAMION)
PUNTO=I

enviar()
{
  /etc/weon/Dropbox-Uploader/dropbox_uploader.sh upload /etc/weon/$1 ArchivosBBB/Informacion/$CAMION.$1
  rm /etc/weon/$1
}
https()
{
	/bin/cat /var/log/syslog|grep weon:$1$PUNTO>/etc/weon/https.log
        LASTIP='8.8.8.8'
	MACFILE=$(echo $1 | sed 's/:/_/g')

	while read line
	do
		IP=`echo $line | awk -F" " '{print $12}'`
		IP=`echo $IP | awk -F"=" '{print $2}'`
		IP="${IP##*( )}"
		
		if [ $IP != $LASTIP ]; then
			LASTIP=$IP
			echo $IP>>/etc/weon/$MACFILE.https
                fi
	done </etc/weon/https.log
	enviar $MACFILE.https
}
#copia el log a un archivo temporal
#https 2c:b4:3a:a1:62:46
while read linea
do
	mac=`echo $linea | awk -F"|" '{print $2}'`
	https $mac
done </etc/weon/InciosSesion.txt

#sube todos los archivos
enviar "InciosSesion.txt"
enviar "Registro.txt"
enviar "squid.log"

#elimina el syslog
rm /var/log/syslog

/sbin/shutdown -r now
