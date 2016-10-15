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
import weon_utils

class weon_daemonize():

    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/var/log/weon_daemon/system.log'
        self.stderr_path = '/var/log/weon_daemon/system.log'
        self.pidfile_path =  '/var/run/weon_daemon/daemon_interface.pid'
        self.pidfile_timeout = 5
        self.check_services =  0
        self.report = 0
        self.threads = dict()
        self.jobs = []

    def _weon_user(self,logger):
        logger.info("Start service for user connections")
        user_management = multiprocessing.Process(target=weon_user_management.start_service, args=(logger,))
        user_management.start()
        self.jobs.append(user_management)

    def _thread_logs(self,logger):
        if not self.threads:
            logger.info( "Create threads for status, gps and active"  )
            self.threads["active_log"] = weon_threads.active_thread(0,"active_log", self.weon_connection, logger)
            self.threads["status_log"] = weon_threads.status_thread(1, "status_log", self.weon_connection, logger)
            self.threads["gps_log"] = weon_threads.gps_thread(2, "gps_log", self.weon_connection, logger)

            [ self.threads[thread_log].start() for  thread_log  in self.threads.keys() ]

    def _check_thread_logs(self,logger):
        if self.threads["active_log"].isAlive():
            logger.info( "%s is Alive" % self.threads["active_log"].getName()  )
        else:
            self.threads["active_log"] = ""
            self.threads["active_log"] = weon_threads.active_thread(0,"active_log", self.weon_connection, logger)
            self.threads["active_log"].start()

        if self.threads["status_log"].isAlive():
            logger.info( "%s is Alive" % self.threads["status_log"].getName() )
        else:
            self.threads["status_log"] = ""
            self.threads["status_log"] = weon_threads.status_thread(1, "status_log", self.weon_connection, logger)
            self.threads["status_log"].start()

        if self.threads["gps_log"].isAlive():
            logger.info( "%s is Alive" % self.threads["gps_log"].getName() )
        else:
            self.threads["gps_log"] = ""
            self.threads["gps_log"] = weon_threads.gps_thread(2, "gps_log", self.weon_connection, logger)
            self.threads["gps_log"].start()



    def run(self):

        self.weon_connection = weon_utils.read_conf_file()

        while True:
            if not self.jobs:
                self._weon_user(logger)
            try:
                if urllib2.urlopen('http://www.google.com',timeout=9):

                    if not self.check_services:
                        self.check_services  = weon_utils.check_services(logger)

                    if not self.report:
                        self.report = weon_utils.reporter(self.weon_connection, logger)

                    self._thread_logs(logger)
                    self._check_thread_logs(logger)
                    time.sleep(1)

                else:
                    logger.info("Unable to connect: %s " % datetime.datetime.now())
                    time.sleep(60)

            except urllib2.URLError:
                logger.info("Lost connection")
                if self.threads:
                    weon_threads.exit()
                    time.sleep(60)
                    [ logger.info("%s - %s" %(self.threads[thread_log].isAlive(),self.threads[thread_log].getName())) for  thread_log  in self.threads.keys()  ]
                    [ thread.join() for  thread  in self.threads  if self.threads[thread].isAlive == True ]
                    self.threads = []
                    weon_threads.start()
                self.check_services = 0
                time.sleep(5)
                continue

logger = logging.getLogger("WeOn Log")
logger.setLevel(logging.INFO)
ftpd = weon_daemonize()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/var/log/weon_daemon/weon_daemon.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

daemon_runner = runner.DaemonRunner(ftpd)
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()
