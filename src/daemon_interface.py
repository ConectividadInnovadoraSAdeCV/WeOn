#!/usr/bin/python

import logging
import time
import datetime
import urllib2
import os
import sys

#third party libs
from daemon import runner

sys.path.append(os.path.join(os.path.dirname(__file__), '/home/rock/WeOn/src/ClientMod'))
import ftptransfer


class ftp_daemonize():

    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/var/run/ftpdaemon/ftp_daemon_service.pid'
        self.pidfile_timeout = 5

    def run(self):
        while True:
            if urllib2.urlopen('http://www.google.com',timeout=1):
                now = datetime.datetime.now()
                t = now.time().hour
                busID = "1114"
                ftpObj = ftptransfer.transfer_ftp(busID,"A1:B2:D6:44")
                ftpObj.connect()
                ftpObj.write_log("connection")
                ftpObj.close()
                #PENDING
                if t > 5 and t < 8:
                    upload_logs_status()

                time.sleep(30)
                ftpObj.connect()
                ftpObj.write_log("url")
                time.sleep(10)
                ftpObj.write_log("active")
                ftpObj.close()
                #upload_status()
                #upload_gps_position()
                #upload_bus_traffic()

            else:
                logger.warn("Unable to connect: %s " % datetime.datetime.now())
                time.sleep(60)

ftpd = ftp_daemonize()
logger = logging.getLogger("DaemonLog")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/var/log/ftpdaemon/ftpdaemon.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

daemon_runner = runner.DaemonRunner(ftpd)
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()
