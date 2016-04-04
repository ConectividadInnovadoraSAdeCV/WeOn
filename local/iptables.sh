# /bin/bash

SQUIDIP=192.168.1.250
SQUIDPORT=3128
iptables -F
iptables -X
iptables -Z
iptables -t nat -F

sysctl net.ipv4.ip_forward=1

#se colocan las politicas por defecto

iptables -P FORWARD DROP

#politicas para redirecciionamiento
iptables -t nat -A POSTROUTING -o ppp0 -j MASQUERADE

#deniego primero los sitios conocidos
iptables -I FORWARD -p tcp -m string --string "youtube.com" --algo kmp -j DROP
iptables -I FORWARD -p tcp -m string --string "netflix.com" --algo kmp -j DROP


#la posicion para la regla que acepta el redireccionamiento
echo '2' > /etc/weon/IptablesRulesPositions.txt

#manejo de estados para aceptar el tráfico que regresa y todo a los dns
iptables -A FORWARD -d 10.34.44.36 -j ACCEPT
iptables -A FORWARD -d 10.182.29.164 -j ACCEPT

iptables -A FORWARD -m state --state ESTABLISHED -j ACCEPT  #esta regla acepta la respuesta de los servidores a la LAN
#iptables -A FORWARD -p tcp -m state --state NEW -m multiport --dports http,https -j LOG --log-prefix "weon" --log-level 4


#esta regla reenvia todo de weon.mx a la bbb
iptables -t nat -A PREROUTING -s $SQUIDIP -p tcp --dport 80 -j ACCEPT
iptables -t nat -A PREROUTING -p tcp --dport http -j DNAT --to 192.168.1.250:8080
iptables -t nat -A PREROUTING -p tcp --dport https -j DNAT --to 192.168.1.250:443


#iptables -t nat -A PREROUTING -p tcp --dport http -j DNAT --to 192.168.1.250:8080
#iptables -t nat -A PREROUTING -p tcp --dport https -j DNAT --to 192.168.1.250:443

#iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination $SQUIDIP:$SQUIDPORT
iptables -t mangle -A PREROUTING -p tcp --dport $SQUIDPORT -j DROP

#iptables -t nat -A PREROUTING -d weon.mx -p tcp --dport 80 -j DNAT --to 192.168.1.250:8080
#iptables -t nat -A PREROUTING -p tcp --dport http -j DNAT --to 192.168.1.250:8080
#iptables -t nat -A PREROUTING -p tcp --dport https -j DNAT --to 192.168.1.250:443


echo "Reglas configuradas"


