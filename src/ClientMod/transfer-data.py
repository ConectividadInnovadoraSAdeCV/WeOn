#!/usr/bin/python

import io
import sys
import datetime
import random

from ftplib import FTP

if  len(sys.argv) > 3:
    busID = sys.argv[1]
    mac_address = sys.argv[2]
    log_type = sys.argv[3]
    date = datetime.date.today()
else:
    print "Unable to save logs without bus identifier"
    exit(1)

class transfer_ftp(object):
    _logs = { "connection": "%s-Connects.txt" % date,
              "url": "%s-URL.txt" % date,
              "location": "%s-GPS.txt" % date
    }

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
            self.ftp.cwd(busID)
        else:
            print "exists"
            self.ftp.cwd(busID)

    def _check_log_exists(self,reg):
        filelist = []
        self.ftp.retrlines('LIST',filelist.append)
        filelist = [x for x in filelist if  transfer_ftp._logs[log_type] in x]
        if not filelist:
            self.overwrite(transfer_ftp._logs[log_type],reg)
        else:
            self.append(transfer_ftp._logs[log_type],reg)


    def _write_connection_file(self,mac_address,genre):
        year = random.choice(range(1989,2012))
        month = random.choice(range(01,12))
        day = random.choice(range(01,31))
        birthday = "%s-%s-%s" % ( day, month, year )
        register = "%s | %s | %s " % (mac_address, birthday, genre)
        self._check_log_exists(register)

    def _write_url_file(self, mac_address,url):
        self._check_log_exists("%s | %s | %s " % (mac_address, url, current_hour))

    def _write_location_file(self,mac_address):
        register = mac_address + " |   |  |   | "
        self._check_log_exists(register)

    def write_log(self,mac_address,log_type):
        self._check_bus_exists()
        if "connection" in log_type:
            genre = random.choice(["Hombre", "Mujer"])
            self._write_connection_file(mac_address,genre)

        elif "url" in log_type:
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
            self._write_url_file(mac_address,url)

        elif "location" in log_type:
            self._write_location_file(mac_address)
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
        exit(1)


if __name__ == "__main__":
    now = datetime.datetime.now()
    t = now.time()
    current_hour = "%s:%s:%s " %  (t.hour,t.minute,t.second)
    global current_hour

    ftp = transfer_ftp()
    ftp.connect()
    ftp.write_log(mac_address,log_type)
    ftp.close()

