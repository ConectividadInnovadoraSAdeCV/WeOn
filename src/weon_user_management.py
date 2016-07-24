#!/usr/bin/python

import threading
import subprocess
import urllib2
import datetime
import os
import time

from GpsMod import gps_service

CONNECTION_FILE = "/home/rock/WeOn/logs/started_sections.txt"
STATE = "/home/rock/WeOn/logs/state_connections"
OUTPUT_FILE = "/home/rock/WeOn/logs/%s-GPS.txt" % datetime.date.today()

class user_thread(threading.Thread):
    def __init__(self, threadID, mac, mdate, gps_value,logger):
        self.threadLock = threading.Lock()
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.mac_name = mac
        self.start_connection = mdate
        self.end_connection = ""
        self.start_position =  gps_value
        self.end_position = ""
        self.log = logger

    def run(self):
        self.threadLock.acquire()
        self.log.info( "Starting " + self.mac_name)
        self._wait_user()
        self.end_position = gps_service.readgps()
        self.end_connection = get_time()
        self._append_data()
        self._remove_tcp_data()
        self.threadLock.release()

    def _wait_user(self):
        try:
            ip_device = subprocess.check_output('arp -a | grep %s' % self.mac_name, shell=True).split(" ")
            ip_device = ip_device[1]
            self.ip_device = ip_device[1:-1]
            self.log.info(self.ip_device)
            time.sleep(10)

            while not subprocess.Popen(["/bin/ping", "-n","-w5","-c1",self.ip_device],stdout=subprocess.PIPE).wait():
                time.sleep(1)
        except subprocess.CalledProcessError:
            self.log.info("failed")

    def _append_data(self):
        with open(OUTPUT_FILE, "a") as _file:
            _file.write("%s | %s | ( %s  ) | %s | ( %s )\n" % (self.mac_name, self.start_connection,
                                                            self.start_position, self.end_connection,
                                                            self.end_position))

    def _remove_tcp_data(self):
        try:
            subprocess.check_output("sh /home/rock/WeOn/src/clean_ip.sh %s %s" % (self.mac_name, self.ip_device) , shell=True)
        except subprocess.CalledProcessError:
            pass



def get_time():
    return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

def get_last_mac():
    return subprocess.check_output('tail -1 %s ' % CONNECTION_FILE , shell=True).rstrip()

def start_service(logger):
    modified_date = ""
    threads = []
    count = 0

    if os.path.exists(STATE):
        f =open(STATE, 'r')
        modified_date = f.readline().rstrip()
        f.close()

    while True:
        if os.path.exists(CONNECTION_FILE):
            tfile = time.ctime(os.path.getmtime(CONNECTION_FILE)).split()
            if  modified_date == tfile[3]:
                #logger.info("waiting for a device")
                #logger.info( "time: %s-%s" % (modified_date, tfile[3]))
                time.sleep(1)
                continue
            elif not modified_date:
                logger.info("waiting for the first device")
                modified_date = 1
                time.sleep(1)
            else:
                mac_address = get_last_mac().split("|")
                gps_value = gps_service.readgps()
                thread = user_thread(count, mac_address[1], get_time() , gps_value,logger)
                thread.start();
                threads.append(thread)
                modified_date = tfile[3]
                f = open(STATE, 'w')
                f.write(modified_date)
                f.close()
                count += 1
            time.sleep(1)
            logger.info(len(threads))
        time.sleep(2)

