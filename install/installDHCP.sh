#Configure Internet Software Consosortium (ISC) to handle router 

#install missing dependencies
apt-get install isc-dhcp-server

cp config/DHCP_config/isc-dhcp-server /etc/default/isc-dhcp-server
cp config/DHCP_config/dhcpd.conf /etc/dhcp/dhcpd.conf
