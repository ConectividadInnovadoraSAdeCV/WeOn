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
mv install/package/LogSite.tar /var/www
cp src/www/001-default /etc/apache2/sites-enabled/001-default
cp src/www/000-default /etc/apache2/sites-enabled/000-default

cd /var/www
rm index.htm
tar xvf LogSite.tar --wildcards '*'

mkdir html
tar -xvf LogSite.tar -C index.htm

#reinicia apache
service apache2 restart
