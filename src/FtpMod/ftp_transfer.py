#!/usr/bin/python

import io
import sys
import datetime
import random

from ftplib import FTP

date = datetime.date.today()

class transfer_ftp:
    logs = { "location": "gps",
              "active" : "active",
              "status" : "status"}

    def __init__(self, busID, mac_address=None,server=None,user=None,password=None ):
        self.busID =  busID
        self.mac = mac_address
        self.server = 'ftp.smarterasp.net'
        self.user = "weonweon"
        self.password= "weonweon"
        self.ftp_main_path = "Logs/Bus/"
        self.ftp_bus_path = self.ftp_main_path + self.busID + "/"

    def connect(self):
        self.ftp = FTP(self.server)
        self.ftp.login(self.user,self.password)

    def _check_bus_exists(self):
        self.ftp.cwd(self.ftp_main_path)
        filelist = []
        self.ftp.retrlines('LIST',filelist.append)
        filelist = [_file for _file in filelist if self.busID in _file]
        if not filelist:
            self.ftp.mkd(self.busID)
            self.ftp.cwd(self.busID)
        else:
            self.ftp.cwd(self.busID)

    def _check_log_exists(self,reg):
        filelist = []
        self.ftp.retrlines('LIST',filelist.append)
        filelist = [_file for _file in filelist if  transfer_ftp._logs[self.log_type] in _file]
        if not filelist:
            self.overwrite(transfer_ftp._logs[self.log_type],reg)
        else:
            self.append(transfer_ftp._logs[self.log_type],reg)

    def _write_location_file(self,location):
        now = datetime.datetime.now()
        current_hour = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        register = "%s | %s" % (location, current_hour)
        self.overwrite(transfer_ftp._logs[self.log_type],register)

    def _write_active_log(self,active):
        now = datetime.datetime.now()
        t = now.time()
        current_hour = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        register = "%s | %s " %  (active,current_hour)
        self.overwrite(transfer_ftp._logs[self.log_type],register)

    def _write_status_log(self,status):
        current_hour = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        current_status = "%s | %s " %  (status,current_hour)
        self.overwrite(transfer_ftp._logs[self.log_type],current_status)

    def write_log(self,log_type,status=None,location=None,active=None):
        self._check_bus_exists()
        if log_type:
            self.log_type = log_type

        if "location" in self.log_type:
            self._write_location_file(location)
        elif "active" in self.log_type:
            self._write_active_log(active)
        elif "status" in self.log_type:
            self._write_status_log(status)
        else:
            print "unable to write"

    def overwrite(self,log_file,data):
        content = io.BytesIO(data + '\n')
        self.ftp.storbinary('STOR %s' % log_file,content)

    def append(self,log_file,data):
        content = io.BytesIO(data + '\n')
        self.ftp.storbinary('APPE %s' % log_file, content)


    def close(self):
        self.ftp.close()
