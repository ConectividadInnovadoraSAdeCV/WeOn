#Configure rules for the BAM devices

apt-get install -y ppp usb-modeswitch usbutils

sed -i "816i # weon Alcatel OneTOuch l100G" /lib/udev/rules.d/40-usb_modeswitch.rules
sed  -i "817i ATTRS{idVendor}==\"1bbb\", ATTRS{idProduct}==\"011e\", RUN+=\"usb_modeswitch '%b/%k'\"\n" /lib/udev/rules.d/40-usb_modeswitch.rules

cp config/BAM/BAM.conf /etc/usb_modeswitch.d/1bbb\:011e

#configure ppp file
cp config/BAM/gprs /etc/ppp/gprs
cp config/BAM/gprs /etc/ppp/peers/gprs


#password for LTE netwoking(4G)
#echo '"wegprs" * "webgprs2002"'>>/etc/ppp/chap-secrets
#echo '"wegprs" * "webgprs2002"'>>/etc/ppp/pap-secrets

