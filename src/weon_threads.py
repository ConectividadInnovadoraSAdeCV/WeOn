#!/usr/bin/python

import threading
import subprocess
import time
import os

from FtpMod import ftp_transfer
from GpsMod import gps_service

class status_thread(threading.Thread):
    def __init__(self, threadID, name, busID):
        self.threadLock = threading.Lock()
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.busID = busID
    def run(self):
        self.threadLock.acquire()
        print "Starting " + self.name
        self.wait_mac(55)
        self.threadLock.release()

    def wait_mac(self,delay):
        GREEN = 5
        YELLOW = 12
        RED = 13
        status = 0
        ftpObj = ftp_transfer.transfer_ftp(self.busID)

        while True:
            connections = subprocess.check_output('arp -a |grep -v incomplete', shell=True).split("\n")
            num_conn = (len(connections) - 1)
            print num_conn
            if num_conn < GREEN:
                if  not status  or status != "G":
                    ftpObj.connect()
                    ftpObj.write_log("status","G",None,None)
                    ftpObj.close()
                    status =  "G"
            if num_conn > GREEN and len(connections) < RED:
                if  not status  or status != "Y":
                    ftpObj.connect()
                    ftpObj.write_log("status","Y",None,None)
                    ftpObj.close()
                    status =  "Y"
            if num_conn > RED:
                if  not status  or status != "R":
                    ftpObj.connect()
                    ftpObj.write_log("status","R",None,None)
                    ftpObj.close()
                    status =  "R"
            time.sleep(delay)
            subprocess.check_output('ip -s -s neigh flush all', shell=True)
            time.sleep(10)


class gps_thread(threading.Thread):
    def __init__(self, threadID, name, busID):
        self.threadLock = threading.Lock()
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.busID = busID
    def run(self):
        self.threadLock.acquire()
        print "Starting " + self.name
        self.gps_position(10)
        self.threadLock.release()

    def gps_position(self,delay):
        ftpObj = ftp_transfer.transfer_ftp(self.busID)
        ftpObj.connect()
        while True:
           ftpObj.connect()
           gps_value = gps_service.readgps()
           ftpObj.write_log("location",None,gps_value,None)
           ftpObj.close()
           time.sleep(delay)

class active_thread(threading.Thread):
    def __init__(self, threadID, name, busID):
        self.threadLock = threading.Lock()
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.busID = busID
    def run(self):
        self.threadLock.acquire()
        print "Starting " + self.name
        self.active_system(300)
        self.threadLock.release()

    def active_system(self,delay):
        ftpObj = ftp_transfer.transfer_ftp(self.busID)
        status = 1
        count = 1
        while True:
            ftpObj.connect()
            ftpObj.write_log("active",None,None,status)
            ftpObj.close()
            while count != delay:
                if os.path.exists("/sys/class/gpio/gpio166/value"):
                    f =open('/sys/class/gpio/gpio166/value', 'r')
                    value = f.read(1)
                    if value == "1":
                        status = 0
                        ftpObj.connect()
                        ftpObj.write_log("active",None,None,status)
                        ftpObj.close()
                        subprocess.check_output('halt', shell=True)
                time.sleep(1)
                count =+ 1
