<?php
	$ip=$_SERVER['REMOTE_ADDR'];
	$arp="/usr/sbin/arp ".$ip;
	$line=shell_exec($arp);
	$lines=split(" ", $line);
	$mac=$lines[59];//aqui esta la mac addreess
	
	
	#El logeo lo pondre en otra linea
	
	$cmd="check:echo '".$mac."|".$_POST["sexo"]."|".$_POST["año"]."".$_POST["mes"]."".$_POST["dia"]."' >> /etc/weon/Registro.txt";
	$handler=fsockopen("localhost",7000);
	if(!$handler)
	{
		header("location: index.html");
	}
	fputs($handler,$cmd);
	fclose($handle);
	/*
	$registro="echo '".date("H",time())."|".$mac."' >> /usr/weon/IniciosSesion.txt";
	$aux=shell_exec($registro);
	*/
	//se trata de llamar a el demonio por cuestiones de permisos
	$cmd="weon:".$mac;
	$manejador=fsockopen("localhost",7000);
	if(!$manejador)
	{
		header("location: index.html");
	}
	fputs($manejador,$cmd);
	while(!feof($manejador))
	{
		$resultado.=fgetc($manejador);
	}
	fputs($manejador, "E");
	fclose($manejador);
	echo $resultado;
	header("Location: http://www.weon.mx/PuntoJaliscoAbierto/descargar.html");
?>