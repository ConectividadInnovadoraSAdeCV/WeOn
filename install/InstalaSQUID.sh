#remplaza el paso 10 del 5.0.0
cd package
#descomprime
tar xvf squid-3.3.10.tar.gz
#entr a squid
cd squid-3.3.10
#configurar squid
./configure --enable-eui
#compliar squid
make all
#instalar squid
make install
#Descarga Squid conf: 
/etc/weon/Dropbox-Uploader/dropbox_uploader.sh download ArchivosBBB/squid.conf /usr/local/squid/etc/squid.conf
# hacer transparente
/etc/weon/Dropbox-Uploader/dropbox_uploader.sh download ArchivosBBB/sysctl.conf /etc/sysctl.conf 

