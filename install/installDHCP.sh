#Configure Internet Software Consosortium (ISC) to handle router 

#install missing dependencies
apt-get install -y isc-dhcp-server

cp config/DHCP/isc-dhcp-server /etc/default/isc-dhcp-server
cp config/DHCP/dhcpd.conf /etc/dhcp/dhcpd.conf
