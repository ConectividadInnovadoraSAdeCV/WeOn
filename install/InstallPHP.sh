
apt-get install -y php5-common libapache2-mod-php5 php5-cli 

apt-get install -y apache2 openssl

mkdir -p /etc/ssl/localcerts

openssl req -new -x509 -days 365 -nodes -out /etc/ssl/localcerts/apache.pem -keyout /etc/ssl/localcerts/apache.key

chmod 600 /etc/ssl/localcerts/apache*

a2enmod ssl

cp src/PortalMod/001-default /etc/apache2/sites-enabled/001-default
cp src/PortalMod/000-default /etc/apache2/sites-enabled/000-default

cd /var/www
rm index.htm

mkdir html
tar -xvf LogSite.tar -C html
cd /home/rock/WeOn
cp src/PortalMod/* /var/www/
cp src/PortalMod/*  /var/www/html/

echo "ServerName localhost" >> /etc/apache2/apache2.conf
a2enmod rewrite

service apache2 restart
