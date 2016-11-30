<?php
    $ip=$_SERVER['REMOTE_ADDR'];
    $arp="/usr/sbin/arp ".$ip;
    $line=shell_exec($arp);
    $lines=split(" ", $line);
    $mac=$lines[59];
    $filename='/home/rock/WeOn/logs/'.date('Y-m-d').'-Connects.txt';
    $cmd=$mac." | ".$_POST["año"]."-".$_POST["mes"]."-".$_POST["dia"]." | ".$_POST["sexo"]."\n";

    $fp = fopen($filename , 'a');
    fwrite($fp, $cmd);
    fclose($fp);
    $mac_test=shell_exec("iptables -L | grep -iP \"ACCEPT.*".$mac."\"");
    if (isset($mac_test)) {
        header("Location: ".$_SERVER['SERVER_NAME'] );
        exit;  }

    $handler=fsockopen("localhost",7000);
    $resultado="";
    fputs($handler,$mac);
    while(!feof($handler))
    {
        $resultado.=fgetc($handler);
    }
    fclose($handler);
    echo $resultado;
    header("Location: http://socialideas.mx/cQ6JA/weon/");
    exit;
?>
