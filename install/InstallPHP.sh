
apt-get install php5-common libapache2-mod-php5 php5-cli 

apt-get install apache2 openssl

mkdir -p /etc/ssl/localcerts

openssl req -new -x509 -days 365 -nodes -out /etc/ssl/localcerts/apache.pem -keyout /etc/ssl/localcerts/apache.key

chmod 600 /etc/ssl/localcerts/apache*

a2enmod ssl

mv install/package/LogSite.tar /var/www
cp src/PortalMod/001-default /etc/apache2/sites-enabled/001-default
cp src/PortalMod/000-default /etc/apache2/sites-enabled/000-default

cd /var/www
rm index.htm
tar xvf LogSite.tar --wildcards '*'

mkdir html
tar -xvf LogSite.tar -C html
cd /home/rock/WeOn
cp src/PortalMod/work.php /var/www/work.php
cp src/PortalMod/work.php  /var/www/html/work.php

echo "ServerName localhost" >> /etc/apache2/apache2.conf
a2enmod rewrite

service apache2 restart
