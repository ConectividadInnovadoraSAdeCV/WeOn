wget http://www.squid-cache.org/Versions/v3/3.5/squid-3.5.18.tar.gz

#descomprime
tar -xvf squid-3.5.18.tar.gz
cd squid-3.5.18
./configure --prefix=/usr/local/squid
#compliar squid
make all
#instalar squid
make install
#Descarga Squid conf: 
cd /home/rock/WeOn
cp config/squid.conf /usr/local/squid/etc/squid.conf
# hacer transparente
cp config/sysctl.conf /etc/sysctl.conf 

