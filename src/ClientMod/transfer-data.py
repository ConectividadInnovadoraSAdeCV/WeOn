#!/usr/bin/python

import io
import sys
import pycurl
from StringIO import StringIO
import datetime

import ftplib
from ftplib import FTP

if  len(sys.argv) > 3:
    busID = sys.argv[1]
    mac_adress = sys.argv[2]
    log_type = sys.argv[3]
else:
    print "Unable to save logs without bus identifier"
    exit(1)

logs = { "access_log": "%s-Connects.txt" % busID,
        "web_page_log": "%s-URL.txt" % busID,
        "user_location_log": "%s-GPS.txt" % busID
        }

class transfer_ftp(object):

    def __init__(self):
        self.server = 'ftp.smarterasp.net'
        self.user = "weonweon"
        self.password= "weonweon"
        self.ftp_main_path = "Logs/Bus/"
        self.ftp_bus_path = self.ftp_main_path + busID + "/"

    def connect(self):
        self.ftp = FTP(self.server)
        self.ftp.login(self.user,self.password)

    def _check_bus_exists(self):
        self.ftp.cwd(self.ftp_main_path)
        filelist = []
        self.ftp.retrlines('LIST',filelist.append)
        filelist = [x for x in filelist if busID in x]
        if not filelist:
            self.ftp.mkd(busID)
            self.ftp.cwd(self.ftp_bus_path)
        else:
            self.ftp.cwd(busID)

    def _check_log_exists(self,reg):
        filelist = []
        self.ftp.retrlines('LIST',filelist.append)
        filelist = [x for x in filelist if logs["access_log"] in x]
        if not filelist:
            content = io.BytesIO(reg)
            self.ftp.storbinary('STOR %s' % logs["access_log"],content)
        else:
            content = io.BytesIO(reg + '\n')
            self.ftp.storbinary('APPE %s' % logs["access_log"],content)


    def _write_connection_file(self,mac_adress):
        now = datetime.datetime.now()
        d = now.date()
        t = now.time()

        register = "%s | %s | %s " % (mac_adress, d,t)

        self._check_log_exists(register)

    def write_log(self,mac_adress,log_type):
        self._check_bus_exists()
        if "connection" in log_type:
            self._write_connection_file(mac_adress)
        elif "url" in log_type:
            self._write_url_file(mac_adress)
        elif "location" in log_type:
            self._write_location_file(mac_adress)
        else:
            print "unable to write"


    def close(self):
        self.ftp.close()
        exit(1)



ftp = transfer_ftp()
ftp.connect()
ftp.write_log(mac_adress,log_type)
ftp.close()

