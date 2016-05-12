#!/usr/bin/python

import logging
import time
import datetime
import urllib2

#third party libs
from daemon import runner

class ftp_daemonize():

    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/var/run/testdaemon/ftp_daemon_service.pid'
        self.pidfile_timeout = 5

    def run(self):
        while True:
            if urllib2.urlopen('http://www.google.com',timeout=1):
                now = datetime.datetime.now()
                t = now.time().hour
                #PENDING
                if t > 5 and t < 8:
                    upload_logs_status()
                upload_status()
                upload_gps_position()
                upload_bus_traffic()

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
