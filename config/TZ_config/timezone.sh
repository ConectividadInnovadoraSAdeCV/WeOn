apt-get install tzdata --reinstall
cp config/TZ_config/Mexico_City /etc/timezone
dpkg-reconfigure tzdata
