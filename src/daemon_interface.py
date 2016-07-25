#!/usr/bin/python

import logging
import time
import datetime
import urllib2
import os
import sys
import subprocess

from daemon import runner
import multiprocessing
import weon_threads
import weon_user_management

busID = "1002"

class weon_daemonize():

    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/var/log/weon_daemon/system.log'
        self.stderr_path = '/var/log/weon_daemon/system.log'
        self.pidfile_path =  '/var/run/weon_daemon/daemon_interface.pid'
        self.pidfile_timeout = 5
        self.threads = []
        self.jobs = []

    def run(self):
        while True:
            if not self.jobs:
                logger.info("Start service for user connections")
                user_management = multiprocessing.Process(target=weon_user_management.start_service, args=(logger,))
                user_management.start()
                self.jobs.append(user_management)
            try:
                subprocess.check_output("bash /home/rock/WeOn/src/check_squid_service.sh %s" % busID,shell=True)
            except:
                logger.info( "SQUID SERVER: OK" )
            try:
                if urllib2.urlopen('http://www.google.com',timeout=9):
                    try:
                        subprocess.check_output("bash /home/rock/WeOn/src/report_files.sh %s" % busID,shell=True)
                    except subprocess.CalledProcessError:
                        logger.info( "SHOULD NOT BE HERE" )

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

            except:
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

logger = logging.getLogger("Daemon Log")
logger.setLevel(logging.INFO)
ftpd = weon_daemonize()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/var/log/weon_daemon/weon_daemon.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

daemon_runner = runner.DaemonRunner(ftpd)
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()
