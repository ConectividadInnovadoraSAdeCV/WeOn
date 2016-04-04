#remplaza el punto 9 de Pasos 5.0.0
#php
apt-get install php5-common libapache2-mod-php5 php5-cli 
#ssl
apt-get install apache2 openssl
#cert
mkdir -p /etc/ssl/localcerts
#crear cert
openssl req -new -x509 -days 365 -nodes -out /etc/ssl/localcerts/apache.pem -keyout /etc/ssl/localcerts/apache.key
#permisos
chmod 600 /etc/ssl/localcerts/apache*
#ae2
a2enmod ssl
#descomprimir sitio
cd /var/www
tar xvf LogSite.tar --wildcards '*'
#descarga sitio 1
/etc/weon/Dropbox-Uploader/dropbox_uploader.sh download ArchivosBBB/001-default /etc/apache2/sites-enabled/001-default
#descarga sitio 2
/etc/weon/Dropbox-Uploader/dropbox_uploader.sh download ArchivosBBB/000-default /etc/apache2/sites-enabled/000-default
#reinicia apache
service apache2 restart
