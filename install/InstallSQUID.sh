wget http://www.squid-cache.org/Versions/v3/3.5/squid-3.5.21.tar.gz

apt-get install libpcap-dev libltdl-dev

tar -xvf squid-3.5.21.tar.gz
cd squid-3.5.21
./configure --prefix=/usr/local/squid

make all -j 4

make install

chown -R rock /usr/local/squid/

cd /home/rock/WeOn
cp config/squid.conf /usr/local/squid/etc/squid.conf

cp config/sysctl.conf /etc/sysctl.conf 

/usr/local/squid/sbin/squid -z
