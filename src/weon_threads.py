#!/usr/bin/python

import threading
import subprocess
import time
import os

from FtpMod import ftp_transfer


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
        self.wait_mac(10)
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
                    ftpObj.write_log("status","G")
                    ftpObj.close()
                    status =  "G"
            if num_conn > GREEN and len(connections) < RED:
                if  not status  or status != "Y":
                    ftpObj.connect()
                    ftpObj.write_log("status","Y")
                    ftpObj.close()
                    status =  "Y"
            if num_conn > RED:
                if  not status  or status != "R":
                    ftpObj.connect()
                    ftpObj.write_log("status","R")
                    ftpObj.close()
                    status =  "R"
            time.sleep(delay)
            subprocess.check_output('ip -s -s neigh flush all', shell=True)
