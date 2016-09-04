<?php
	$ip=$_SERVER['REMOTE_ADDR'];
	$arp="/usr/sbin/arp ".$ip;
	$line=shell_exec($arp);
	$lines=split(" ", $line);
	$mac=$lines[59];//aqui esta la mac addreess
	$filename='/home/rock/WeOn/logs/'.date('Y-m-d').'-Connects.txt';
    $cmd=$mac." | ".$_POST["año"]."-".$_POST["mes"]."-".$_POST["dia"]." | ".$_POST["sexo"]."\n";

    $fp = fopen($filename , 'a');
    fwrite($fp, $cmd);
    fclose($fp);
	//se trata de llamar a el demonio por cuestiones de permisos
	$manejador=fsockopen("localhost",7000);
	if(!$manejador)
	{
		header("location: index.html");
	}
        $resultado="";
	fputs($manejador,$mac);
	while(!feof($manejador))
	{
		$resultado.=fgetc($manejador);
	}
	fputs($manejador, "E");
    fclose($manejador);
        echo $resultado;
	header("Location: http://www.weon.mx/PuntoJaliscoAbierto/descargar.html");
?>
