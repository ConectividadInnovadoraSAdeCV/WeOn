#remplaza el paso 13 del 5.0.0 configurar la BAM
#Configure rules for the BAM devices
cp config/40-usb_modeswitch.rules /lib/udev/rules.d/40-usb_modeswitch.rules
#cp config/BAM_Config/BAM.conf /etc/usb_modeswitch.d/1bbb\:011e
cp config/BAM_Config/BAM.conf /etc/usb_modeswitch.d/1bbb\:f017

#install ppp
apt-get install netbase ifupdown ppp

#configure ppp file
cp config/BAM_Config/gprs /etc/ppp/gprs
cp config/BAM_Config/gprs /etc/ppp/peers/gprs


#password for LTE netwoking(4G)
echo '"Iusacellgsm" * "iusacellgsm"'>>/etc/ppp/chap-secrets
echo '"Iusacellgsm" * "iusacellgsm"'>>/etc/ppp/pap-secrets

