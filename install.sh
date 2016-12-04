
cp config/File_system/hosts /etc/hosts

echo 'set completion-ignore-case On' >> /home/rock/.inputrc
echo "export PATH=$PATH:~/opt/bin:/sbin/:/usr/sbin" >> /home/rock/.bashrc
ln -sf /usr/share/zoneinfo/America/Mexico_City /etc/localtime

git config --global core.editor vim 
git config --global color.ui true
git config --global color.branch true
git config --global color.diff true
git config --global color.interactive true
git config --global color.status true
git config --global color.diff.meta "blue black bold"


apt-get install -y vim git
apt-get install -y build-essential
apt-get install -y ntp  ntpdate curl
aptitude install -y conntrack

ntpdate 129.6.15.28

mkdir -p /home/rock/WeOn/logs
chmod 7777 -R /home/rock/WeOn/logs

date +"%Y-%m-%d" > /home/rock/WeOn/logs/report.txt

sh install/l100g.sh
sh install/installDHCP.sh
sh install/InstallPHP.sh
sh install/InstallFTP.sh
sh install/InstallSQUID.sh
