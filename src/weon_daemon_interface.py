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
import weon_test

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
        self.user_management = ""

    def _weon_user(self,logger):
        if not self.user_management:
            logger.info("Start service for user connections")
            self.user_management = multiprocessing.Process(target=weon_user_management.start_service, args=(logger,))
            self.user_management.start()

    def _thread_logs(self,logger):
        if not self.threads:
            logger.info( "Create threads for status, gps and active"  )
            self.threads["active_log"] = weon_threads.active_thread(0,"active_log", self.weon_connection, logger)
            self.threads["status_log"] = weon_threads.status_thread(1, "status_log", self.weon_connection, logger)
            self.threads["gps_log"] = weon_threads.gps_thread(2, "gps_log", self.weon_connection, logger)

            [ self.threads[thread_log].start() for  thread_log  in self.threads.keys() ]

    def _check_thread_logs(self,logger):
        if not self.threads["active_log"].isAlive():
            self.threads["active_log"] = ""
            self.threads["active_log"] = weon_threads.active_thread(0,"active_log", self.weon_connection, logger)
            self.threads["active_log"].start()

        if not self.threads["status_log"].isAlive():
            self.threads["status_log"] = ""
            self.threads["status_log"] = weon_threads.status_thread(1, "status_log", self.weon_connection, logger)
            self.threads["status_log"].start()

        if not self.threads["gps_log"].isAlive():
            self.threads["gps_log"] = ""
            self.threads["gps_log"] = weon_threads.gps_thread(2, "gps_log", self.weon_connection, logger)
            self.threads["gps_log"].start()

    def _check_weon_user_process( self, logger ):
        if not self.user_management.is_alive():
            self.user_management = ""

    def run(self):

        self.weon_connection = weon_utils.read_conf_file()

        while True:
            try:
                if urllib2.urlopen('http://www.google.com',timeout=9):
                    if not self.check_services:
                        self.check_services  = weon_utils.check_services(logger)
                        weon_test.gps_testing( logger )

                    if not self.report:
                        self.report = weon_utils.reporter(self.weon_connection, logger)

                    self._weon_user(logger)
                    self._thread_logs(logger)
                    self._check_thread_logs(logger)
                    self._check_weon_user_process( logger )
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
                    self.threads = dict()
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
