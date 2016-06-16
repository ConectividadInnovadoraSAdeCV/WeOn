#!/usr/bin/python

import logging
import time
import datetime
import urllib2
import os
import sys

from daemon import runner
from FtpMod import ftp_transfer
from GpsMod import gps_service
import weon_threads

busID = "1000"

class weon_daemonize():

    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/var/log/weon_daemon/system.log'
        self.stderr_path = '/var/log/weon_daemon/system.log'
        self.pidfile_path =  '/var/run/weon_daemon/daemon_interface.pid'
        self.pidfile_timeout = 5
        self.threads = []

    def run(self):
        while True:
            try:
                if urllib2.urlopen('http://www.google.com',timeout=9):
                    if not self.threads:
                        logger.info( "Create threas for status, gps and active")

                        active_thread = weon_threads.active_thread(0,"active_log",busID)
                        state_thread = weon_threads.status_thread(1, "status_log",busID)
                        gps_thread = weon_threads.gps_thread(2, "gps_log", busID)

                        active_thread.start()
                        state_thread.start()
                        gps_thread.start()

                        self.threads.append( active_thread )
                        self.threads.append( state_thread )
                        self.threads.append( gps_thread )

                    logger.info(self.threads[0].isAlive())
                    time.sleep(5)
                    self.threads[0].join(1)
                    #now = datetime.datetime.now()
                    #t = now.time().hour

                else:
                    logger.warn("Unable to connect: %s " % datetime.datetime.now())
                    time.sleep(60)
            except urllib2.URLError:
                if self.threads:
                    time.sleep(30)

ftpd = weon_daemonize()
logger = logging.getLogger("Daemon Log")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/var/log/weon_daemon/weon_daemon.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

daemon_runner = runner.DaemonRunner(ftpd)
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()
