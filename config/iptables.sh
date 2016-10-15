# /bin/bash

SQUIDIP=192.168.1.250
SQUIDPORT=3128
iptables -F
iptables -X
iptables -Z
iptables -t nat -F

sysctl net.ipv4.ip_forward=1

iptables -P FORWARD DROP

iptables -t nat -A POSTROUTING -o ppp0 -j MASQUERADE

iptables -A FORWARD -d 8.8.8.8 -j ACCEPT
iptables -A FORWARD -d 8.8.4.4 -j ACCEPT


iptables -A FORWARD -m state --state ESTABLISHED  -j ACCEPT
iptables -t nat -A PREROUTING -s $SQUIDIP -p tcp --dport 80 -j ACCEPT

iptables -t nat -A PREROUTING -p tcp --dport http -j DNAT --to 192.168.1.250
iptables -t nat -A PREROUTING -p tcp --dport https -j DNAT --to 192.168.1.250:443
iptables -t mangle -A PREROUTING -p tcp --dport 8080 -j DROP



echo "Reglas configuradas"


