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
                        logger.info( "Create threads for status, gps and active")

                        active_thread = weon_threads.active_thread(0,"active_log",busID,logger)
                        state_thread = weon_threads.status_thread(1, "status_log",busID,logger)
                        gps_thread = weon_threads.gps_thread(2, "gps_log", busID,logger)

                        self.threads.extend( (active_thread,state_thread, gps_thread) )

                        [ thread.start() for  thread  in self.threads ]

                    [ logger.info("%s - %s" %(thread.isAlive(),thread.getName())) for  thread  in self.threads ]
                    time.sleep(5)

                else:
                    logger.info("Unable to connect: %s " % datetime.datetime.now())
                    time.sleep(60)

            except urllib2.URLError:
                logger.info("Lost connection")
                if self.threads:
                    weon_threads.exit()
                    time.sleep(60)
                    [ logger.info("%s - %s" %(thread.isAlive(),thread.getName())) for  thread  in self.threads  ]
                    [ thread.join() for  thread  in self.threads   ]
                    self.threads = []
                    weon_threads.start()
                time.sleep(5)
                continue




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
