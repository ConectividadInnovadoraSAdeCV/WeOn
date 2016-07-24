
cp config/fs_config/hosts /etc/hosts

echo 'set completion-ignore-case On' >> /home/rock/.inputrc
echo "export PATH=$PATH:~/opt/bin:/sbin/:/usr/sbin" >> /home/rock/.bashrc
ln -sf /usr/share/zoneinfo/America/Mexico_City /etc/localtime


git config --global user.name "Paul Barajas"
git config --global user.email paul.barajas@linux.com
git config --global core.editor vim 
git config --global color.ui true
git config --global color.branch true
git config --global color.diff true
git config --global color.interactive true
git config --global color.status true
git config --global color.diff.meta "blue black bold"


apt-get install vim git
apt-get install build-essential
apt-get install ntp  ntpdate curl

ntpdate 129.6.15.28


mkdir -p /home/rock/WeOn/logs
chmod 7777 -R /home/rock/WeOn/logs

date +"%Y-%m-%d" > /home/rock/WeOn/logs/report.txt

sh install/l100g.sh
sh install/installDHCP.sh
sh install/InstallPHP.sh
sh install/InstallFTP.sh
sh install/InstallSQUID.sh

g++ src/weon_mac_service.cpp -o weon_mac_service
mv weon_mac_service bin/

