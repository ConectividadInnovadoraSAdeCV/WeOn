#Configure rules for the BAM devices

sed -i "977i # weon Alcatel OneTOuch l100G" /lib/udev/rules.d/40-usb_modeswitch.rules
sed "978i ATTR{idVendor}==\"1bbb\", ATTR{idProduct}==\"011e\", RUN+=\"usb_modeswitch '%b/%k'\"" /lib/udev/rules.d/40-usb_modeswitch.rules

cp config/BAM_Config/BAM.conf /etc/usb_modeswitch.d/1bbb\:011e

#configure ppp file
cp config/BAM_Config/gprs /etc/ppp/gprs
cp config/BAM_Config/gprs /etc/ppp/peers/gprs


#password for LTE netwoking(4G)
echo '"Iusacellgsm" * "iusacellgsm"'>>/etc/ppp/chap-secrets
echo '"Iusacellgsm" * "iusacellgsm"'>>/etc/ppp/pap-secrets

