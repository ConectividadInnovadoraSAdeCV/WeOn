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
from status_thread import weon_threads

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
            if urllib2.urlopen('http://www.google.com',timeout=2):
                if not self.threads:
                    logger.info( "Create threas for status, gps and active")
                    state_thread = status_thread(1, "status_log",busID)
                    state_thread.start()
                    self.threads.append( state_thread )
                logger.info(self.threads[0].isAlive())
                time.sleep(5)
                #now = datetime.datetime.now()
                #t = now.time().hour

            else:
                logger.warn("Unable to connect: %s " % datetime.datetime.now())
                time.sleep(60)

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
