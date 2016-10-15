#!/bin/bash

MAC=$1
IP=$2

iptables -D FORWARD -m mac --mac-source $MAC -j ACCEPT
iptables -t nat -D PREROUTING  -m mac --mac-source $MAC -j ACCEPT
iptables -t nat -D PREROUTING -m mac --mac-source $MAC -p tcp --dport 80 -j DNAT --to-destination 192.168.1.250:3128

conntrack -D --orig-src $IP
arp -d $IP
