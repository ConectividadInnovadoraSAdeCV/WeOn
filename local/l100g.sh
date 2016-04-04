#remplaza el paso 13 del 5.0.0 configurar la BAM
#modfica las reglas
/etc/weon/Dropbox-Uploader/dropbox_uploader.sh download ArchivosBBB/40-usb_modeswitch.rules /lib/udev/rules.d/40-usb_modeswitch.rules
#descarga el archivo de configuracion
/etc/weon/Dropbox-Uploader/dropbox_uploader.sh download ArchivosBBB/BAM.conf /etc/usb_modeswitch.d/1bbb\:011e
#instala ppp
apt-get install netbase ifupdown ppp
#descarga conf de grps
etc/weon/Dropbox-Uploader/dropbox_uploader.sh download ArchivosBBB/gprs /etc/ppp/gprs
/etc/weon/Dropbox-Uploader/dropbox_uploader.sh download ArchivosBBB/gprs /etc/ppp/peers/gprs
#coloco las contaraseñas de la red 4g
echo '"wegprs" * "webgprs2002"'>>/etc/ppp/chap-secrets
echo '"wegprs" * "webgprs2002"'>>/etc/ppp/pap-secrets

