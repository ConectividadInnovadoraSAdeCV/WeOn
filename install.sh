
apt-get install vim git 
apt-get install build-essential
apt-get install ntp  ntpdate

ntpdate 129.6.15.28


mkdir -p /home/rock/WeOn/logs
chmod 7777 -R /home/rock/WeOn/logs
sh install/l100g.sh
sh install/installDHCP.sh
sh install/InstallPHP.sh
sh install/InstallFTP.sh
sh install/InstallSQUID.sh
