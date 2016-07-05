cd package
#descomprime
tar -xvf squid-3.3.10.tar.gz
#entr a squid
cd squid-3.3.10
#configurar squid
./configure --prefix=/usr/local/squid
#compliar squid
make all
#instalar squid
make install
#Descarga Squid conf: 
cp config/squid.conf /usr/local/squid/etc/squid.conf
# hacer transparente
cp config/sysctl.conf /etc/sysctl.conf 

