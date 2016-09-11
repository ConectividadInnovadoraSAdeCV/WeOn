#!/bin/bash

MAC=$1

iptables -A FORWARD -m mac --mac-source $MAC -j ACCEPT
iptables -t nat -I PREROUTING -m mac --mac-source $MAC -j ACCEPT
iptables -t nat -I PREROUTING -m mac --mac-source $MAC -p tcp --dport 80 -j DNAT --to-destination 192.168.1.250:3128
