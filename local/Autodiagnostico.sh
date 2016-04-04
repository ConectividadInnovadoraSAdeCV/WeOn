#!bash
#cada 10 minutos
ArchivoTemporal=/etc/weon/eth0Status
DiagnosticaNuevamente(){
ifconfig eth0>$ArchivoTemporal
        if grep '250' $ArchivoTemporal;then
           printf 'Todo en orden'
        else
          printf 'IP Incorrecta 2 veces, se reiniciara'
          /sbin/reboot
        fi

}
DiagnosticaRed(){
        ifconfig eth0>$ArchivoTemporal
	if grep '250' $ArchivoTemporal;then
	   printf 'Todo en orden'
        else
	  printf 'IP Incorrecta'
	  /etc/init.d/networking restart
	fi
}
DiagnosticaRed
DiagnosticaRed
DiagnosticaRed
DiagnosticaNuevamente

