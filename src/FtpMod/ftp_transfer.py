#!/usr/bin/python

import io
import sys
import datetime
import random

from ftplib import FTP

date = datetime.date.today()

class transfer_ftp:
    _logs = { "connection": "%s-Connects.txt" % date,
              "url": "%s-URL.txt" % date,
              "location": "%s-GPS.txt" % date,
              "active" : "active",
              "status" : "status",
    }

    def __init__(self, busID, mac_address=None):
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
        filelist = [x for x in filelist if self.busID in x]
        if not filelist:
            self.ftp.mkd(self.busID)
            self.ftp.cwd(self.busID)
        else:
            self.ftp.cwd(self.busID)

    def _check_log_exists(self,reg):
        filelist = []
        self.ftp.retrlines('LIST',filelist.append)
        filelist = [x for x in filelist if  transfer_ftp._logs[self.log_type] in x]
        if not filelist:
            self.overwrite(transfer_ftp._logs[self.log_type],reg)
        else:
            self.append(transfer_ftp._logs[self.log_type],reg)


    def _write_connection_file(self,genre):
        year = random.choice(range(1989,2012))
        month = random.choice(range(01,12))
        day = random.choice(range(01,31))
        birthday = "%s-%s-%s" % ( day, month, year )
        register = "%s | %s | %s " % (self.mac, birthday, genre)
        self._check_log_exists(register)

    def _write_url_file(self,url):
        now = datetime.datetime.now()
        t = now.time()
        current_hour = "%s:%s:%s " %  (t.hour,t.minute,t.second)
        self._check_log_exists("%s | %s | %s " % (self.mac, url, current_hour))

    def _write_location_file(self):
        register = self.mac + " |   |  |   | "
        self._check_log_exists(register)

    def _write_active_log(self):
        now = datetime.datetime.now()
        t = now.time()
        current_hour = "%s:%s:%s " %  (t.hour,t.minute,t.second)
        self.overwrite(transfer_ftp._logs[self.log_type],current_hour)
    def _write_status_log(self,status):
        now = datetime.datetime.now()
        t = now.time()
        current_status = "%s | %s:%s:%s " %  (status,t.hour,t.minute,t.second)
        self.overwrite(transfer_ftp._logs[self.log_type],current_status)

    def write_log(self,log_type,status=None):
        self._check_bus_exists()
        if log_type:
            self.log_type = log_type
        if "connection" in self.log_type:
            genre = random.choice(["Hombre", "Mujer"])
            self._write_connection_file(genre)
        elif "url" in self.log_type:
            url = random.choice(["www.google.com","www.youtube.com",
                   "www.netflix.com","www.weon.mx",
                   "www.linux.com","www.opensource.org",
                   "www.freesoftwarefoundation.org,www.gnu.org",
                   "www.forbes.com","www.facebook.com",
                   "www.greenpeace.org","stackoverflow.com/how_to_read",
                   "www.gmail.com","www.perl.org",
                   "www.python.com","www.hello-world.gnu",
                   "www.test.org","www.atomix.vg",
                   "www.gps-coordinates.net","ibiblio.org",
                   "www.campus-party.mx","www.haveaniceday.com"])
            self._write_url_file(url)

        elif "location" in self.log_type:
            self._write_location_file()
        elif "active" in self.log_type:
            self._write_active_log()
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
